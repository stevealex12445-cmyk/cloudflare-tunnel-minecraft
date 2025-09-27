import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import shutil, socket, random

def find_free_port(start=20000, end=30000):
    while True:
        port = random.randint(start, end)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

class TunnelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Cloudflare Tunnel")
        self.geometry("600x400")

        self.hostname = tk.StringVar()
        self.local_port = 25565
        self.proc = None

        ttk.Label(self, text="请输入服务器域名:").pack(pady=10)
        ttk.Entry(self, textvariable=self.hostname, width=40).pack()

        self.btn_start = ttk.Button(self, text="连接服务器", command=self.start_tunnel)
        self.btn_start.pack(pady=10)

        self.btn_stop = ttk.Button(self, text="断开连接", command=self.stop_tunnel, state=tk.DISABLED)
        self.btn_stop.pack(pady=10)

        self.log = tk.Text(self, height=12)
        self.log.pack(fill=tk.BOTH, expand=True)

        # 启动时检测 cloudflared
        self.check_cloudflared()

    def check_cloudflared(self):
        if not shutil.which("cloudflared"):
            self.log.insert(tk.END, "未检测到 cloudflared，请先安装:\n")
            self.log.insert(tk.END, "下载地址: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation\n")
            messagebox.showwarning("缺少 cloudflared", "未检测到 cloudflared，请先安装！")
        else:
            self.log.insert(tk.END, "已检测到 cloudflared，可正常使用。\n")

    def start_tunnel(self):
        host = self.hostname.get().strip()
        if not host:
            messagebox.showerror("错误", "请输入域名")
            return

        # 检查端口占用
        if is_port_in_use(25565):
            self.local_port = find_free_port()
            self.log.insert(tk.END, f"⚠️ 25565 已被占用，改用随机端口 {self.local_port}\n")
        else:
            self.local_port = 25565
            self.log.insert(tk.END, "使用默认端口 25565\n")

        cmd = [
            "cloudflared", "access", "tcp",
            "--hostname", host,
            f"--url", f"127.0.0.1:{self.local_port}"
        ]

        def run():
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.log.insert(tk.END, f"隧道已启动，请在 Minecraft 中使用 127.0.0.1:{self.local_port}\n")
            for line in self.proc.stdout:
                self.log.insert(tk.END, line)
                self.log.see(tk.END)

        threading.Thread(target=run, daemon=True).start()

    def stop_tunnel(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.log.insert(tk.END, "隧道已断开。\n")
        messagebox.showinfo("提示", "隧道已断开。")

if __name__ == "__main__":
    TunnelApp().mainloop()
