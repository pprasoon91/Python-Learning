#!/usr/bin/env python3
"""
Ubuntu IDM Clone - Download Manager
Enhanced version with fixes and additional features
"""

import sys
import os
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import json
import threading
from dataclasses import dataclass, asdict
from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLineEdit, QProgressBar, QLabel, 
                            QListWidget, QListWidgetItem, QTextEdit, QTabWidget,
                            QFileDialog, QSystemTrayIcon, QMenu, QMessageBox,
                            QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
                            QDialog, QFormLayout, QSpinBox, QCheckBox)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt, QSettings, QSize
from PyQt6.QtGui import QIcon, QAction, QColor
from PyQt6.QtWidgets import QStyle

# Constants
DEFAULT_CHUNKS = 8
MAX_CONCURRENT_DOWNLOADS = 3
VIDEO_SITES = [
    'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
    'facebook.com', 'instagram.com', 'twitter.com', 'tiktok.com'
]

@dataclass
class DownloadItem:
    """Represents a download item with all its properties"""
    url: str
    filename: str
    save_path: str
    total_size: int = 0
    downloaded_size: int = 0
    status: str = "waiting"  # waiting, downloading, paused, completed, failed
    speed: float = 0.0
    chunks: int = DEFAULT_CHUNKS
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    paused: bool = False
    video_options: Optional[Dict] = None
    
    @property
    def progress(self) -> float:
        if self.total_size > 0:
            return (self.downloaded_size / self.total_size) * 100
        return 0.0

class SettingsDialog(QDialog):
    """Settings dialog window"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.default_path_edit = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_path)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.default_path_edit)
        path_layout.addWidget(self.browse_button)
        
        self.chunks_spin = QSpinBox()
        self.chunks_spin.setRange(1, 32)
        self.chunks_spin.setValue(DEFAULT_CHUNKS)
        
        self.max_downloads_spin = QSpinBox()
        self.max_downloads_spin.setRange(1, 10)
        self.max_downloads_spin.setValue(MAX_CONCURRENT_DOWNLOADS)
        
        self.dark_mode_check = QCheckBox("Enable Dark Mode")
        
        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add to form
        layout.addRow("Default Download Path:", path_layout)
        layout.addRow("Download Chunks:", self.chunks_spin)
        layout.addRow("Max Concurrent Downloads:", self.max_downloads_spin)
        layout.addRow(self.dark_mode_check)
        layout.addRow(button_layout)
        
    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Default Download Folder")
        if folder:
            self.default_path_edit.setText(folder)

class DownloadEngine:
    """Enhanced download engine with multi-threading and pause/resume support"""
    
    def __init__(self):
        self.active_downloads: Dict[str, DownloadItem] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.paused = False
        
    async def start_session(self):
        """Initialize aiohttp session"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            headers={'User-Agent': 'Ubuntu-IDM-Clone/2.0'}
        )
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def is_video_site(self, url: str) -> bool:
        """Check if URL is from a known video site"""
        return any(site in url.lower() for site in VIDEO_SITES)
    
    async def get_file_info(self, url: str) -> Dict:
        """Get file information from URL"""
        try:
            async with self.session.head(url, allow_redirects=True) as response:
                headers = response.headers
                return {
                    'size': int(headers.get('content-length', 0)),
                    'accepts_ranges': headers.get('accept-ranges', '').lower() == 'bytes',
                    'filename': self._extract_filename(url, headers),
                    'content_type': headers.get('content-type', 'application/octet-stream')
                }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return {'size': 0, 'accepts_ranges': False, 'filename': Path(url).name}
    
    def _extract_filename(self, url: str, headers: Dict) -> str:
        """Extract filename from URL or headers"""
        content_disposition = headers.get('content-disposition', '')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"\'')
            return filename
        return Path(url).name or 'download'
    
    async def extract_video_info(self, url: str) -> Dict:
        """Extract video information using yt-dlp"""
        def extract_sync():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if info:
                        formats = []
                        for f in info.get('formats', []):
                            if f.get('filesize'):
                                formats.append({
                                    'format_id': f['format_id'],
                                    'ext': f['ext'],
                                    'resolution': f.get('resolution', 'unknown'),
                                    'filesize': f['filesize'],
                                    'format_note': f.get('format_note', ''),
                                })
                        
                        return {
                            'title': info.get('title', 'Unknown'),
                            'formats': formats,
                            'uploader': info.get('uploader', 'Unknown'),
                            'thumbnail': info.get('thumbnail', ''),
                            'duration': info.get('duration', 0),
                        }
            except Exception as e:
                print(f"Error extracting video info: {e}")
                return None
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, extract_sync)
    
    async def download_video(self, url: str, download_item: DownloadItem, progress_callback=None):
        """Download video using yt-dlp with selected options"""
        def download_sync():
            try:
                output_path = Path(download_item.save_path)
                output_path.mkdir(parents=True, exist_ok=True)
                
                download_item.status = "downloading"
                download_item.start_time = datetime.now().isoformat()
                
                ydl_opts = {
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'progress_hooks': [self._create_progress_hook(download_item, progress_callback)],
                    'quiet': True,
                    'no_warnings': True,
                }
                
                # Apply video options if specified
                if download_item.video_options:
                    ydl_opts.update(download_item.video_options)
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            except Exception as e:
                download_item.status = "failed"
                print(f"Video download failed: {e}")
                if progress_callback:
                    progress_callback(download_item)
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            await loop.run_in_executor(executor, download_sync)
    
    def _create_progress_hook(self, download_item: DownloadItem, progress_callback):
        """Create progress hook for yt-dlp downloads"""
        def progress_hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                if total_bytes > 0:
                    download_item.total_size = total_bytes
                    download_item.downloaded_size = downloaded_bytes
                    download_item.status = "downloading"
                    
                    speed = d.get('speed', 0)
                    if speed:
                        download_item.speed = speed
                    
                    if progress_callback:
                        progress_callback(download_item)
            
            elif d['status'] == 'finished':
                download_item.status = "completed"
                download_item.downloaded_size = download_item.total_size
                download_item.end_time = datetime.now().isoformat()
                
                if progress_callback:
                    progress_callback(download_item)
        
        return progress_hook
    
    async def download_chunk(self, url: str, start: int, end: int, chunk_file: str, download_item: DownloadItem):
        """Download a specific chunk of the file with pause support"""
        headers = {'Range': f'bytes={start}-{end}'}
        
        try:
            async with self.session.get(url, headers=headers) as response:
                async with aiofiles.open(chunk_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        while download_item.paused:
                            await asyncio.sleep(0.5)
                        
                        await f.write(chunk)
                        download_item.downloaded_size += len(chunk)
        except Exception as e:
            print(f"Error downloading chunk {chunk_file}: {e}")
            raise
    
    async def download_file(self, download_item: DownloadItem, progress_callback=None):
        """Download file with chunked downloading or video extraction"""
        if self.is_video_site(download_item.url):
            await self._handle_video_download(download_item, progress_callback)
        else:
            await self._handle_regular_download(download_item, progress_callback)
    
    async def _handle_video_download(self, download_item: DownloadItem, progress_callback):
        """Handle video site downloads"""
        video_info = await self.extract_video_info(download_item.url)
        if not video_info:
            download_item.status = "failed"
            return
        
        # Set filename based on video title
        title = video_info.get('title', 'video')
        clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        download_item.filename = f"{clean_title}.mp4"  # Default to mp4
        
        await self.download_video(download_item.url, download_item, progress_callback)
    
    async def _handle_regular_download(self, download_item: DownloadItem, progress_callback):
        """Handle regular file downloads"""
        file_info = await self.get_file_info(download_item.url)
        download_item.total_size = file_info['size']
        
        output_path = Path(download_item.save_path) / download_item.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_info['accepts_ranges'] and file_info['size'] > 1024 * 1024:
            await self._chunked_download(download_item, progress_callback)
        else:
            await self._simple_download(download_item, progress_callback)
    
    async def _chunked_download(self, download_item: DownloadItem, progress_callback):
        """Download file in chunks with pause support"""
        url = download_item.url
        output_path = Path(download_item.save_path) / download_item.filename
        chunk_size = download_item.total_size // download_item.chunks
        
        chunk_files = []
        tasks = []
        
        for i in range(download_item.chunks):
            start = i * chunk_size
            end = start + chunk_size - 1
            if i == download_item.chunks - 1:
                end = download_item.total_size - 1
            
            chunk_file = f"{output_path}.part{i}"
            chunk_files.append(chunk_file)
            
            task = self.download_chunk(url, start, end, chunk_file, download_item)
            tasks.append(task)
        
        download_item.status = "downloading"
        download_item.start_time = datetime.now().isoformat()
        
        try:
            await asyncio.gather(*tasks)
            
            if not download_item.paused:
                await self._merge_chunks(chunk_files, output_path)
                download_item.status = "completed"
                download_item.end_time = datetime.now().isoformat()
            else:
                download_item.status = "paused"
            
        except Exception as e:
            download_item.status = "failed"
            print(f"Download failed: {e}")
        finally:
            if download_item.status == "completed":
                for chunk_file in chunk_files:
                    if os.path.exists(chunk_file):
                        os.remove(chunk_file)
    
    async def _simple_download(self, download_item: DownloadItem, progress_callback):
        """Simple download without chunking"""
        url = download_item.url
        output_path = Path(download_item.save_path) / download_item.filename
        
        download_item.status = "downloading"
        download_item.start_time = datetime.now().isoformat()
        
        try:
            async with self.session.get(url) as response:
                async with aiofiles.open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        while download_item.paused:
                            await asyncio.sleep(0.5)
                        
                        await f.write(chunk)
                        download_item.downloaded_size += len(chunk)
                        
                        if progress_callback:
                            progress_callback(download_item)
            
            if not download_item.paused:
                download_item.status = "completed"
                download_item.end_time = datetime.now().isoformat()
            else:
                download_item.status = "paused"
            
        except Exception as e:
            download_item.status = "failed"
            print(f"Download failed: {e}")
    
    async def _merge_chunks(self, chunk_files: List[str], output_path: Path):
        """Merge downloaded chunks into final file"""
        async with aiofiles.open(output_path, 'wb') as output_file:
            for chunk_file in chunk_files:
                if os.path.exists(chunk_file):
                    async with aiofiles.open(chunk_file, 'rb') as chunk:
                        content = await chunk.read()
                        await output_file.write(content)

class DownloadWorker(QThread):
    """Enhanced Qt Worker thread for handling downloads with queue management"""
    progress_updated = pyqtSignal(str, dict)  # download_id, progress_data
    download_completed = pyqtSignal(str)  # download_id
    download_failed = pyqtSignal(str, str)  # download_id, error_message
    download_paused = pyqtSignal(str)  # download_id
    
    def __init__(self, max_concurrent_downloads=MAX_CONCURRENT_DOWNLOADS):
        super().__init__()
        self.engine = DownloadEngine()
        self.downloads_queue = asyncio.Queue()
        self.active_downloads = set()
        self.running = True
        self.max_concurrent_downloads = max_concurrent_downloads
        self.paused_downloads = set()
    
    def add_download(self, download_item: DownloadItem):
        """Add download to queue"""
        asyncio.run_coroutine_threadsafe(
            self.downloads_queue.put(download_item), 
            self.loop
        )
    
    def pause_download(self, download_id: str):
        """Pause a download"""
        asyncio.run_coroutine_threadsafe(
            self._pause_download(download_id),
            self.loop
        )
    
    async def _pause_download(self, download_id: str):
        """Internal pause download implementation"""
        for download in self.engine.active_downloads.values():
            if download.url == download_id:
                download.paused = True
                download.status = "paused"
                self.paused_downloads.add(download_id)
                self.download_paused.emit(download_id)
                break
    
    def resume_download(self, download_id: str):
        """Resume a paused download"""
        asyncio.run_coroutine_threadsafe(
            self._resume_download(download_id),
            self.loop
        )
    
    async def _resume_download(self, download_id: str):
        """Internal resume download implementation"""
        if download_id in self.paused_downloads:
            for download in self.engine.active_downloads.values():
                if download.url == download_id:
                    download.paused = False
                    download.status = "downloading"
                    self.paused_downloads.remove(download_id)
                    # Re-add to queue to continue downloading
                    await self.downloads_queue.put(download)
                    break
    
    def run(self):
        """Main worker thread loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def worker():
            await self.engine.start_session()
            
            while self.running:
                try:
                    # Limit concurrent downloads
                    if len(self.active_downloads) >= self.max_concurrent_downloads:
                        await asyncio.sleep(1)
                        continue
                    
                    # Wait for download with timeout
                    download_item = await asyncio.wait_for(
                        self.downloads_queue.get(), timeout=1.0
                    )
                    
                    # Skip if already active
                    if download_item.url in self.active_downloads:
                        continue
                    
                    self.active_downloads.add(download_item.url)
                    
                    def progress_callback(item):
                        self.progress_updated.emit(item.url, asdict(item))
                    
                    await self.engine.download_file(download_item, progress_callback)
                    
                    self.active_downloads.remove(download_item.url)
                    
                    if download_item.status == "completed":
                        self.download_completed.emit(download_item.url)
                    elif download_item.status == "failed":
                        self.download_failed.emit(download_item.url, "Download failed")
                        
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"Worker error: {e}")
            
            await self.engine.close_session()
        
        self.loop.run_until_complete(worker())

class VideoOptionsDialog(QDialog):
    """Dialog for selecting video download options"""
    def __init__(self, video_info: Dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Download Options")
        self.setModal(True)
        self.video_info = video_info
        self.selected_format = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Video info
        info_group = QWidget()
        info_layout = QFormLayout(info_group)
        
        title_label = QLabel(self.video_info.get('title', 'Unknown'))
        uploader_label = QLabel(self.video_info.get('uploader', 'Unknown'))
        duration_label = QLabel(self.format_duration(self.video_info.get('duration', 0)))
        
        info_layout.addRow("Title:", title_label)
        info_layout.addRow("Uploader:", uploader_label)
        info_layout.addRow("Duration:", duration_label)
        
        # Format selection
        self.format_combo = QComboBox()
        for fmt in self.video_info.get('formats', []):
            self.format_combo.addItem(
                f"{fmt.get('resolution', '?')} - {fmt.get('format_note', '')} ({fmt.get('ext', '?')}, {self.format_size(fmt.get('filesize', 0))})",
                fmt['format_id']
            )
        
        # Buttons
        self.download_button = QPushButton("Download")
        self.cancel_button = QPushButton("Cancel")
        
        self.download_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add to layout
        layout.addWidget(info_group)
        layout.addWidget(QLabel("Select Format:"))
        layout.addWidget(self.format_combo)
        layout.addLayout(button_layout)
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS"""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_selected_format(self) -> Dict:
        """Get the selected video format options"""
        format_id = self.format_combo.currentData()
        return {
            'format': format_id,
            'ext': 'mp4',  # Prefer mp4 format
        }

class MainWindow(QMainWindow):
    """Enhanced main application window with additional features"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UbuntuIDM', 'DownloadManager')
        self.downloads = {}
        self.max_concurrent_downloads = MAX_CONCURRENT_DOWNLOADS
        self.dark_mode = False
        
        self.init_ui()
        self.setup_worker()
        self.setup_system_tray()
        self.load_settings()
        
        # Start worker thread
        self.worker.start()
    
    def init_ui(self):
        """Initialize the enhanced user interface"""
        self.setWindowTitle("Ubuntu Download Manager")
        self.setGeometry(100, 100, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter download URL...")
        self.browse_button = QPushButton("Browse...")
        self.download_button = QPushButton("Download")
        self.settings_button = QPushButton("Settings")
        
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.browse_button)
        url_layout.addWidget(self.download_button)
        url_layout.addWidget(self.settings_button)
        
        layout.addLayout(url_layout)
        
        # Downloads table
        self.downloads_table = QTableWidget()
        self.downloads_table.setColumnCount(7)
        self.downloads_table.setHorizontalHeaderLabels([
            "Filename", "Size", "Progress", "Speed", "Status", "Path", "Actions"
        ])
        
        # Configure table
        header = self.downloads_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.downloads_table)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.download_button.clicked.connect(self.start_download)
        self.browse_button.clicked.connect(self.browse_save_location)
        self.settings_button.clicked.connect(self.show_settings)
        self.url_input.returnPressed.connect(self.start_download)
        
        # Apply initial style
        self.apply_style()
    
    def setup_worker(self):
        """Setup and configure the worker thread"""
        self.worker = DownloadWorker(self.max_concurrent_downloads)
        self.worker.progress_updated.connect(self.update_download_progress)
        self.worker.download_completed.connect(self.download_completed)
        self.worker.download_failed.connect(self.download_failed)
        self.worker.download_paused.connect(self.download_paused)
    
    def setup_system_tray(self):
        """Setup system tray icon with enhanced menu"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
            
            tray_menu = QMenu()
            
            show_action = QAction("Show", self)
            pause_all_action = QAction("Pause All", self)
            resume_all_action = QAction("Resume All", self)
            quit_action = QAction("Quit", self)
            
            show_action.triggered.connect(self.show)
            pause_all_action.triggered.connect(self.pause_all_downloads)
            resume_all_action.triggered.connect(self.resume_all_downloads)
            quit_action.triggered.connect(self.close)
            
            tray_menu.addAction(show_action)
            tray_menu.addSeparator()
            tray_menu.addAction(pause_all_action)
            tray_menu.addAction(resume_all_action)
            tray_menu.addSeparator()
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def apply_style(self):
        """Apply dark or light style to the application"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2d2d2d;
                }
                QTableWidget {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    gridline-color: #555555;
                }
                QHeaderView::section {
                    background-color: #353535;
                    color: #ffffff;
                    padding: 5px;
                    border: 1px solid #555555;
                }
                QLineEdit {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #505050;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #606060;
                }
                QProgressBar {
                    border: 1px solid #555555;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                }
            """)
        else:
            self.setStyleSheet("")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.default_path_edit.setText(self.save_path)
        dialog.chunks_spin.setValue(DEFAULT_CHUNKS)
        dialog.max_downloads_spin.setValue(self.max_concurrent_downloads)
        dialog.dark_mode_check.setChecked(self.dark_mode)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.save_path = dialog.default_path_edit.text()
            self.max_concurrent_downloads = dialog.max_downloads_spin.value()
            
            # Update worker with new max concurrent downloads
            self.worker.max_concurrent_downloads = self.max_concurrent_downloads
            
            # Apply dark mode if changed
            new_dark_mode = dialog.dark_mode_check.isChecked()
            if new_dark_mode != self.dark_mode:
                self.dark_mode = new_dark_mode
                self.apply_style()
            
            # Save settings
            self.settings.setValue('save_path', self.save_path)
            self.settings.setValue('max_concurrent_downloads', self.max_concurrent_downloads)
            self.settings.setValue('dark_mode', self.dark_mode)
    
    async def show_video_options(self, url: str) -> Optional[Dict]:
        """Show video options dialog and return selected format"""
        video_info = await self.worker.engine.extract_video_info(url)
        if not video_info or not video_info.get('formats'):
            return None
        
        dialog = VideoOptionsDialog(video_info, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_selected_format()
        return None
    
    def start_download(self):
        """Start a new download with enhanced checks"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL")
            return
        
        if url in self.downloads:
            QMessageBox.information(self, "Info", "Download already exists")
            return
        
        # Create download item
        filename = Path(url).name or "download"
        download_item = DownloadItem(
            url=url,
            filename=filename,
            save_path=self.save_path,
            chunks=DEFAULT_CHUNKS
        )
        
        # Add to downloads table
        row = self.downloads_table.rowCount()
        self.downloads_table.insertRow(row)
        
        # For video URLs, we'll update the filename later
        display_name = "Extracting video info..." if self.is_video_url(url) else filename
        self.downloads_table.setItem(row, 0, QTableWidgetItem(display_name))
        self.downloads_table.setItem(row, 1, QTableWidgetItem("Unknown"))
        
        progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.downloads_table.setCellWidget(row, 2, progress_bar)
        
        self.downloads_table.setItem(row, 3, QTableWidgetItem("0 KB/s"))
        self.downloads_table.setItem(row, 4, QTableWidgetItem("Waiting"))
        self.downloads_table.setItem(row, 5, QTableWidgetItem(self.save_path))
        
        # Add action buttons
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        
        pause_button = QPushButton()
        pause_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        pause_button.setFixedSize(24, 24)
        pause_button.clicked.connect(lambda: self.pause_download(url))
        
        cancel_button = QPushButton()
        cancel_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        cancel_button.setFixedSize(24, 24)
        cancel_button.clicked.connect(lambda: self.cancel_download(url))
        
        action_layout.addWidget(pause_button)
        action_layout.addWidget(cancel_button)
        self.downloads_table.setCellWidget(row, 6, action_widget)
        
        # Store download info
        self.downloads[url] = {
            'item': download_item,
            'row': row,
            'progress_bar': progress_bar,
            'pause_button': pause_button,
            'cancel_button': cancel_button
        }
        
        # For video URLs, show options dialog first
        if self.is_video_url(url):
            asyncio.create_task(self._handle_video_download(url, download_item))
        else:
            # Add to worker queue
            self.worker.add_download(download_item)
        
        # Clear URL input
        self.url_input.clear()
    
    async def _handle_video_download(self, url: str, download_item: DownloadItem):
        """Handle video download with options dialog"""
        video_options = await self.show_video_options(url)
        if video_options:
            download_item.video_options = video_options
            self.worker.add_download(download_item)
        else:
            # Remove from table if user canceled
            if url in self.downloads:
                row = self.downloads[url]['row']
                self.downloads_table.removeRow(row)
                del self.downloads[url]
    
    def pause_download(self, download_id: str):
        """Pause a download"""
        if download_id in self.downloads:
            self.worker.pause_download(download_id)
    
    def resume_download(self, download_id: str):
        """Resume a paused download"""
        if download_id in self.downloads:
            self.worker.resume_download(download_id)
    
    def pause_all_downloads(self):
        """Pause all active downloads"""
        for download_id in self.downloads:
            if self.downloads[download_id]['item'].status == "downloading":
                self.pause_download(download_id)
    
    def resume_all_downloads(self):
        """Resume all paused downloads"""
        for download_id in self.downloads:
            if self.downloads[download_id]['item'].status == "paused":
                self.resume_download(download_id)
    
    def cancel_download(self, download_id: str):
        """Cancel a download"""
        if download_id in self.downloads:
            # For simplicity, we just remove it from the UI
            # In a real app, we'd need to properly cancel the download
            row = self.downloads[download_id]['row']
            self.downloads_table.removeRow(row)
            del self.downloads[download_id]
    
    def is_video_url(self, url: str) -> bool:
        """Check if URL is from a video site"""
        return any(site in url.lower() for site in VIDEO_SITES)
    
    def browse_save_location(self):
        """Browse for save location"""
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.save_path)
        if folder:
            self.save_path = folder
    
    def update_download_progress(self, download_id: str, progress_data: dict):
        """Update download progress in the table"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            progress_bar = download_info['progress_bar']
            
            # Update filename if it changed (for video downloads)
            filename = progress_data.get('filename', '')
            if filename and filename != "video_download":
                self.downloads_table.setItem(row, 0, QTableWidgetItem(filename))
            
            # Update progress bar
            progress = progress_data.get('progress', 0)
            progress_bar.setValue(int(progress))
            
            # Update size
            total_size = progress_data.get('total_size', 0)
            if total_size > 0:
                size_text = f"{self.format_size(total_size)}"
                self.downloads_table.setItem(row, 1, QTableWidgetItem(size_text))
            
            # Update speed
            speed = progress_data.get('speed', 0)
            speed_text = f"{self.format_size(speed)}/s"
            self.downloads_table.setItem(row, 3, QTableWidgetItem(speed_text))
            
            # Update status
            status = progress_data.get('status', 'Unknown')
            self.downloads_table.setItem(row, 4, QTableWidgetItem(status.title()))
            
            # Update pause button icon
            if status == "paused":
                download_info['pause_button'].setIcon(
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            else:
                download_info['pause_button'].setIcon(
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
    
    def download_completed(self, download_id: str):
        """Handle download completion"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            
            self.downloads_table.setItem(row, 4, QTableWidgetItem("Completed"))
            
            # Remove action buttons
            self.downloads_table.removeCellWidget(row, 6)
            
            # Show notification
            if hasattr(self, 'tray_icon'):
                filename = self.downloads[download_id]['item'].filename
                self.tray_icon.showMessage(
                    "Download Complete",
                    f"'{filename}' downloaded successfully",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
    
    def download_failed(self, download_id: str, error_message: str):
        """Handle download failure"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            
            self.downloads_table.setItem(row, 4, QTableWidgetItem("Failed"))
    
    def download_paused(self, download_id: str):
        """Handle download pause"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            
            self.downloads_table.setItem(row, 4, QTableWidgetItem("Paused"))
            
            # Update pause button icon
            download_info['pause_button'].setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def load_settings(self):
        """Load application settings"""
        self.save_path = self.settings.value('save_path', str(Path.home() / "Downloads"))
        self.max_concurrent_downloads = self.settings.value('max_concurrent_downloads', MAX_CONCURRENT_DOWNLOADS, type=int)
        self.dark_mode = self.settings.value('dark_mode', False, type=bool)
        
        # Restore window geometry
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Save settings
        self.settings.setValue('save_path', self.save_path)
        self.settings.setValue('max_concurrent_downloads', self.max_concurrent_downloads)
        self.settings.setValue('dark_mode', self.dark_mode)
        self.settings.setValue('geometry', self.saveGeometry())
        
        # Stop worker thread
        self.worker.running = False
        self.worker.wait()
        
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Ubuntu Download Manager")
    app.setApplicationVersion("2.0")
    
    # Check for system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "System Tray", "System tray is not available on this system.")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()