import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time

# ------------------ CONFIG ------------------
BROADCAST_PORT = 54545
TCP_PORT = 54546
DISCOVERY_INTERVAL = 1.5  # seconds
my_name = socket.gethostname()
known_peers = {}

# ------------------ GUI ------------------
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("LAN Chat")

        tk.Label(master, text=f"My Name: {my_name}").pack()

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack()
        self.listbox.bind("<Double-Button-1>", self.connect_to_peer)

        self.refresh_ui()

    def refresh_ui(self):
        self.listbox.delete(0, tk.END)
        for name, (ip, _) in known_peers.items():
            self.listbox.insert(tk.END, f"{name} ({ip})")
        self.master.after(2000, self.refresh_ui)

    def connect_to_peer(self, event):
        selection = self.listbox.curselection()
        if selection:
            name = list(known_peers.keys())[selection[0]]
            ip, _ = known_peers[name]
            start_chat(ip)

# ------------------ BROADCAST PRESENCE ------------------
def broadcast_presence():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        message = f"{my_name}"
        udp_sock.sendto(message.encode(), ("<broadcast>", BROADCAST_PORT))
        print(f"[BROADCAST] Sent presence as {my_name}")
        time.sleep(DISCOVERY_INTERVAL)

# ------------------ LISTEN FOR BROADCASTS ------------------
def listen_for_broadcasts():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("", BROADCAST_PORT))
    print(f"[INFO] Listening for broadcasts on UDP port {BROADCAST_PORT}...")
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            name = data.decode()
            if name != my_name:
                known_peers[name] = (addr[0], time.time())
                print(f"[DISCOVERY] Found peer: {name} @ {addr[0]}")
        except Exception as e:
            print(f"[ERROR] Broadcast receive error: {e}")

# ------------------ CHAT HANDLING ------------------
def handle_chat(conn, addr):
    chat_window(conn, addr, incoming=True)

def chat_window(conn, addr, incoming):
    def send_msg():
        msg = input_box.get()
        conn.send(msg.encode())
        chat_area.insert(tk.END, f"You: {msg}\n")
        input_box.delete(0, tk.END)

    def receive_loop():
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    break
                chat_area.insert(tk.END, f"{peer_name}: {msg}\n")
            except:
                break

    win = tk.Toplevel()
    peer_name = addr if isinstance(addr, str) else addr[0]
    win.title(f"Chat with {peer_name}")

    chat_area = scrolledtext.ScrolledText(win, width=50, height=15)
    chat_area.pack()

    input_box = tk.Entry(win, width=40)
    input_box.pack(side=tk.LEFT, padx=5)
    tk.Button(win, text="Send", command=send_msg).pack(side=tk.RIGHT, padx=5)

    threading.Thread(target=receive_loop, daemon=True).start()

def start_chat(ip):
    try:
        conn = socket.create_connection((ip, TCP_PORT), timeout=5)
        chat_window(conn, ip, incoming=False)
    except Exception as e:
        print(f"[ERROR] Couldn't connect to {ip}: {e}")

# ------------------ TCP SERVER ------------------
def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", TCP_PORT))
    server.listen(5)
    print(f"[INFO] TCP server running on port {TCP_PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[TCP] Incoming connection from {addr}")
        threading.Thread(target=handle_chat, args=(conn, addr), daemon=True).start()

# ------------------ MAIN ------------------
def main():
    threading.Thread(target=broadcast_presence, daemon=True).start()
    threading.Thread(target=listen_for_broadcasts, daemon=True).start()
    threading.Thread(target=start_tcp_server, daemon=True).start()

    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
