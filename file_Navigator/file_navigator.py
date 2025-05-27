import os
import platform
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import subprocess
import mimetypes

class FileExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cross-Platform File Explorer")
        self.geometry("900x600")
        self.current_path = Path.home()
        self.history = []
        self.create_widgets()
        self.load_directory(self.current_path)

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Type", "Size"), show="tree headings")
        self.tree.heading("#0", text="Name", anchor=tk.W)
        self.tree.heading("Type", text="Type", anchor=tk.W)
        self.tree.heading("Size", text="Size", anchor=tk.W)
        self.tree.column("#0", width=300)
        self.tree.column("Type", width=150)
        self.tree.column("Size", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.on_item_double_click)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(bottom_frame, text="Open Folder", command=self.choose_folder).pack(side=tk.LEFT)
        tk.Button(bottom_frame, text="Back", command=self.go_back).pack(side=tk.LEFT)
        tk.Button(bottom_frame, text="Show All Types", command=self.show_all_types).pack(side=tk.LEFT)


        self.status_label = tk.Label(self, text="Items: 0 | Total Size: 0 Bytes")
        self.status_label.pack(anchor=tk.W, padx=10)

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_path = Path(folder_path)
            self.tree.delete(*self.tree.get_children())
            self.load_directory(self.current_path)

    def load_directory(self, path: Path, save_history=True):
        if save_history:
            self.history.append(self.current_path)
        self.current_path = path

        # ✅ Clear the Treeview here
        self.tree.delete(*self.tree.get_children())

        count = 0
        total_size = 0
        items = []

        for item in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            ftype = self.get_type(item)
            size = "Calculating..." if item.is_dir() else self.format_size(item.stat().st_size)
            items.append((item, ftype, size))
            count += 1
            if item.is_file():
                total_size += item.stat().st_size

        for item, ftype, size in items:
            node = self.tree.insert("", "end", text=item.name, values=(ftype, size))
            self.tree.item(node, tags=(str(item),))

        self.status_label.config(text=f"Items: {count} | Total Size: ~{self.format_size(total_size)}")

        # Background folder size calculation
        threading.Thread(target=self.calculate_folder_sizes, args=(items,), daemon=True).start()


    def calculate_folder_sizes(self, items):
        for item, ftype, _ in items:
            if item.is_dir():
                size = self.get_dir_size(item)
                self.update_item_size(item, size)

    def update_item_size(self, path: Path, size_bytes):
        for item in self.tree.get_children():
            tags = self.tree.item(item, "tags")
            if tags and Path(tags[0]) == path:
                self.tree.set(item, "Size", self.format_size(size_bytes))
                break

    def on_item_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        item_path = Path(self.tree.item(item_id, "tags")[0])
        if item_path.is_dir():
            self.load_directory(item_path, save_history=True)
        else:
            self.open_in_explorer(item_path)

    def get_type(self, path: Path):
        if path.is_dir():
            return "Folder"
        type_guess, _ = mimetypes.guess_type(path)
        return type_guess or "Unknown File"

    def get_dir_size(self, path: Path):
        try:
            return sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
        except Exception:
            return 0

    def format_size(self, size_bytes):
        for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024

    def show_all_types(self):
        files_by_type = {}
        for item in self.tree.get_children():
            path = Path(self.tree.item(item, "tags")[0])
            ftype = self.get_type(path)
            files_by_type.setdefault(ftype, []).append(path.name)

        result = "\n".join(f"{ftype}:\n  " + "\n  ".join(files) for ftype, files in files_by_type.items())
        messagebox.showinfo("Files by Type", result)

    def open_in_explorer(self, path: Path):
        try:
            if platform.system() == "Windows":
                os.startfile(str(path))
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(path)])
            else:
                subprocess.run(["xdg-open", str(path)])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        if self.history:
            previous_path = self.history.pop()
            self.load_directory(previous_path, save_history=False)
        else:
            messagebox.showinfo("Back", "No previous folder to return to.")


if __name__ == "__main__":
    app = FileExplorerApp()
    app.mainloop()
