#!/usr/bin/env python3
"""
Ubuntu IDM Clone - Download Manager
A basic implementation of a download manager similar to IDM for Ubuntu/Linux
"""

import sys
import os
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import List, Optional, Dict
import json
import threading
from dataclasses import dataclass, asdict
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLineEdit, QProgressBar, QLabel, 
                            QListWidget, QListWidgetItem, QTextEdit, QTabWidget,
                            QFileDialog, QSystemTrayIcon, QMenu, QMessageBox,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt, QSettings
from PyQt6.QtGui import QIcon, QAction

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
    chunks: int = 8
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    @property
    def progress(self) -> float:
        if self.total_size > 0:
            return (self.downloaded_size / self.total_size) * 100
        return 0.0

class DownloadEngine:
    """Core download engine with multi-threading support"""
    
    def __init__(self):
        self.active_downloads: Dict[str, DownloadItem] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.video_sites = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'facebook.com', 'instagram.com', 'twitter.com', 'tiktok.com'
        ]
        
    async def start_session(self):
        """Initialize aiohttp session"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            headers={'User-Agent': 'Ubuntu-IDM-Clone/1.0'}
        )
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def is_video_site(self, url: str) -> bool:
        """Check if URL is from a known video site"""
        return any(site in url.lower() for site in self.video_sites)
    
    async def extract_video_info(self, url: str) -> Dict:
        """Extract video information using yt-dlp"""
        import yt_dlp
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def extract_sync():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                    'format': 'best[ext=mp4]/best',  # Prefer mp4 format
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    if info:
                        return {
                            'title': info.get('title', 'Unknown'),
                            'url': info.get('url', ''),
                            'ext': info.get('ext', 'mp4'),
                            'filesize': info.get('filesize', 0) or info.get('filesize_approx', 0),
                            'duration': info.get('duration', 0),
                            'uploader': info.get('uploader', 'Unknown'),
                            'thumbnail': info.get('thumbnail', ''),
                        }
            except Exception as e:
                print(f"Error extracting video info: {e}")
                return None
        
        # Run yt-dlp in a thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, extract_sync)
            return result
    
    async def download_video(self, url: str, download_item: DownloadItem, progress_callback=None):
        """Download video using yt-dlp"""
        import yt_dlp
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        output_path = Path(download_item.save_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Progress hook for yt-dlp
        def progress_hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                if total_bytes > 0:
                    download_item.total_size = total_bytes
                    download_item.downloaded_size = downloaded_bytes
                    download_item.status = "downloading"
                    
                    # Calculate speed
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
        
        def download_sync():
            try:
                download_item.status = "downloading"
                download_item.start_time = datetime.now().isoformat()
                
                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            except Exception as e:
                download_item.status = "failed"
                print(f"Video download failed: {e}")
                if progress_callback:
                    progress_callback(download_item)
        
        # Run yt-dlp in a thread pool to avoid blocking the async loop
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            await loop.run_in_executor(executor, download_sync)
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
        # Try Content-Disposition header first
        content_disposition = headers.get('content-disposition', '')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"\'')
            return filename
        
        # Fallback to URL
        return Path(url).name or 'download'
    
    async def download_chunk(self, url: str, start: int, end: int, chunk_file: str):
        """Download a specific chunk of the file"""
        headers = {'Range': f'bytes={start}-{end}'}
        
        try:
            async with self.session.get(url, headers=headers) as response:
                async with aiofiles.open(chunk_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
        except Exception as e:
            print(f"Error downloading chunk {chunk_file}: {e}")
            raise
    
    async def download_file(self, download_item: DownloadItem, progress_callback=None):
        """Download file with chunked downloading or video extraction"""
        url = download_item.url
        
        # Check if it's a video site URL
        if self.is_video_site(url):
            print(f"Detected video site URL: {url}")
            
            # Extract video information first
            video_info = await self.extract_video_info(url)
            if video_info and video_info.get('url'):
                # Update download item with video info
                title = video_info.get('title', 'video')
                ext = video_info.get('ext', 'mp4')
                
                # Clean filename
                import re
                clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                download_item.filename = f"{clean_title}.{ext}"
                download_item.total_size = video_info.get('filesize', 0)
                
                # Download the video
                await self.download_video(url, download_item, progress_callback)
                return
            else:
                print("Failed to extract video information")
                download_item.status = "failed"
                return
        
        # Regular file download
        output_path = Path(download_item.save_path) / download_item.filename
        
        # Get file information
        file_info = await self.get_file_info(url)
        download_item.total_size = file_info['size']
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_info['accepts_ranges'] and file_info['size'] > 1024 * 1024:  # 1MB threshold
            await self._chunked_download(download_item, progress_callback)
        else:
            await self._simple_download(download_item, progress_callback)
    
    async def _chunked_download(self, download_item: DownloadItem, progress_callback=None):
        """Download file in chunks"""
        url = download_item.url
        output_path = Path(download_item.save_path) / download_item.filename
        chunk_size = download_item.total_size // download_item.chunks
        
        # Create temporary chunk files
        chunk_files = []
        tasks = []
        
        for i in range(download_item.chunks):
            start = i * chunk_size
            end = start + chunk_size - 1
            if i == download_item.chunks - 1:  # Last chunk
                end = download_item.total_size - 1
            
            chunk_file = f"{output_path}.part{i}"
            chunk_files.append(chunk_file)
            
            task = self.download_chunk(url, start, end, chunk_file)
            tasks.append(task)
        
        # Download all chunks concurrently
        download_item.status = "downloading"
        download_item.start_time = datetime.now().isoformat()
        
        try:
            await asyncio.gather(*tasks)
            
            # Merge chunks
            await self._merge_chunks(chunk_files, output_path)
            
            download_item.status = "completed"
            download_item.downloaded_size = download_item.total_size
            download_item.end_time = datetime.now().isoformat()
            
        except Exception as e:
            download_item.status = "failed"
            print(f"Download failed: {e}")
        finally:
            # Clean up chunk files
            for chunk_file in chunk_files:
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
    
    async def _simple_download(self, download_item: DownloadItem, progress_callback=None):
        """Simple download without chunking"""
        url = download_item.url
        output_path = Path(download_item.save_path) / download_item.filename
        
        download_item.status = "downloading"
        download_item.start_time = datetime.now().isoformat()
        
        try:
            async with self.session.get(url) as response:
                async with aiofiles.open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
                        download_item.downloaded_size += len(chunk)
                        
                        if progress_callback:
                            progress_callback(download_item)
            
            download_item.status = "completed"
            download_item.end_time = datetime.now().isoformat()
            
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
    """Qt Worker thread for handling downloads"""
    progress_updated = pyqtSignal(str, dict)  # download_id, progress_data
    download_completed = pyqtSignal(str)  # download_id
    download_failed = pyqtSignal(str, str)  # download_id, error_message
    
    def __init__(self):
        super().__init__()
        self.engine = DownloadEngine()
        self.downloads_queue = asyncio.Queue()
        self.running = True
    
    def add_download(self, download_item: DownloadItem):
        """Add download to queue"""
        asyncio.run_coroutine_threadsafe(
            self.downloads_queue.put(download_item), 
            self.loop
        )
    
    def run(self):
        """Main worker thread loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def worker():
            await self.engine.start_session()
            
            while self.running:
                try:
                    # Wait for download with timeout
                    download_item = await asyncio.wait_for(
                        self.downloads_queue.get(), timeout=1.0
                    )
                    
                    def progress_callback(item):
                        self.progress_updated.emit(item.url, asdict(item))
                    
                    await self.engine.download_file(download_item, progress_callback)
                    
                    if download_item.status == "completed":
                        self.download_completed.emit(download_item.url)
                    else:
                        self.download_failed.emit(download_item.url, "Download failed")
                        
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"Worker error: {e}")
            
            await self.engine.close_session()
        
        self.loop.run_until_complete(worker())

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UbuntuIDM', 'DownloadManager')
        self.downloads = {}
        self.worker = DownloadWorker()
        
        self.init_ui()
        self.setup_worker_connections()
        self.setup_system_tray()
        
        # Start worker thread
        self.worker.start()
        
        # Load settings
        self.load_settings()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Ubuntu Download Manager")
        self.setGeometry(100, 100, 900, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter download URL...")
        self.browse_button = QPushButton("Browse...")
        self.download_button = QPushButton("Download")
        
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.browse_button)
        url_layout.addWidget(self.download_button)
        
        layout.addLayout(url_layout)
        
        # Downloads table
        self.downloads_table = QTableWidget()
        self.downloads_table.setColumnCount(6)
        self.downloads_table.setHorizontalHeaderLabels([
            "Filename", "Size", "Progress", "Speed", "Status", "Path"
        ])
        
        # Make table columns stretch
        header = self.downloads_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.downloads_table)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Connect signals
        self.download_button.clicked.connect(self.start_download)
        self.browse_button.clicked.connect(self.browse_save_location)
        
        # Default download path
        self.save_path = str(Path.home() / "Downloads")
    
    def setup_worker_connections(self):
        """Setup connections to worker thread"""
        self.worker.progress_updated.connect(self.update_download_progress)
        self.worker.download_completed.connect(self.download_completed)
        self.worker.download_failed.connect(self.download_failed)
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            
            tray_menu = QMenu()
            show_action = QAction("Show", self)
            quit_action = QAction("Quit", self)
            
            show_action.triggered.connect(self.show)
            quit_action.triggered.connect(self.close)
            
            tray_menu.addAction(show_action)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def start_download(self):
        """Start a new download"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL")
            return
        
        if url in self.downloads:
            QMessageBox.information(self, "Info", "Download already exists")
            return
        
        # Create download item
        if self.is_video_url(url):
            # For video URLs, we'll get the actual filename after extraction
            filename = "video_download"
        else:
            filename = Path(url).name or "download"
        
        download_item = DownloadItem(
            url=url,
            filename=filename,
            save_path=self.save_path,
            chunks=8
        )
        
        # Add to downloads table
        row = self.downloads_table.rowCount()
        self.downloads_table.insertRow(row)
        
        # Show "Extracting..." for video URLs
        display_name = "Extracting video info..." if self.is_video_url(url) else filename
        self.downloads_table.setItem(row, 0, QTableWidgetItem(display_name))
        self.downloads_table.setItem(row, 1, QTableWidgetItem("Unknown"))
        
        progress_bar = QProgressBar()
        self.downloads_table.setCellWidget(row, 2, progress_bar)
        
        self.downloads_table.setItem(row, 3, QTableWidgetItem("0 KB/s"))
        self.downloads_table.setItem(row, 4, QTableWidgetItem("Waiting"))
        self.downloads_table.setItem(row, 5, QTableWidgetItem(self.save_path))
        
        # Store download info
        self.downloads[url] = {
            'item': download_item,
            'row': row,
            'progress_bar': progress_bar
        }
        
        # Add to worker queue
        self.worker.add_download(download_item)
        
        # Clear URL input
        self.url_input.clear()
    
    def is_video_url(self, url: str) -> bool:
        """Check if URL is from a video site"""
        video_sites = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'facebook.com', 'instagram.com', 'twitter.com', 'tiktok.com'
        ]
        return any(site in url.lower() for site in video_sites)
    
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
    
    def download_completed(self, download_id: str):
        """Handle download completion"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            
            self.downloads_table.setItem(row, 4, QTableWidgetItem("Completed"))
            
            # Show notification
            if hasattr(self, 'tray_icon'):
                self.tray_icon.showMessage(
                    "Download Complete",
                    f"File downloaded successfully",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
    
    def download_failed(self, download_id: str, error_message: str):
        """Handle download failure"""
        if download_id in self.downloads:
            download_info = self.downloads[download_id]
            row = download_info['row']
            
            self.downloads_table.setItem(row, 4, QTableWidgetItem("Failed"))
    
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
        
        # Restore window geometry
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Save settings
        self.settings.setValue('save_path', self.save_path)
        self.settings.setValue('geometry', self.saveGeometry())
        
        # Stop worker thread
        self.worker.running = False
        self.worker.wait()
        
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Ubuntu Download Manager")
    app.setApplicationVersion("1.0")
    
    # Check for system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "System Tray", "System tray is not available on this system.")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()