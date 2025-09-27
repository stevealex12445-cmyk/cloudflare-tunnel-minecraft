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
        self.geometry("700x520")
        self.configure(bg="#0d1b2a")

        self.hostname = tk.StringVar()
        self.local_port = 25565
        self.proc = None

        # ttk 样式
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background="#0d1b2a", foreground="white", font=("Microsoft YaHei", 11))
        style.configure("Card.TFrame", background="#1b263b")
        style.configure("TButton", background="#4fc3f7", foreground="black",
                        font=("Microsoft YaHei", 10, "bold"), padding=6)
        style.map("TButton",
                  background=[("active", "#81d4fa")],
                  foreground=[("active", "black")])
        style.configure("TEntry", fieldbackground="#1b263b", foreground="white", insertcolor="white")

        # 标题
        title = ttk.Label(self, text="⚡ Minecraft Cloudflare Tunnel", 
                          font=("Microsoft YaHei", 14, "bold"), foreground="#4fc3f7")
        title.pack(pady=15)

        # 卡片区域
        card = ttk.Frame(self, style="Card.TFrame", padding=20)
        card.pack(padx=20, pady=10, fill=tk.X)

        ttk.Label(card, text="请输入服务器域名:").pack(anchor="w", pady=5)
        ttk.Entry(card, textvariable=self.hostname, width=40).pack(anchor="w", pady=5)

        btn_frame = ttk.Frame(card, style="Card.TFrame")
        btn_frame.pack(pady=10)

        self.btn_start = ttk.Button(btn_frame, text="连接服务器", command=self.start_tunnel)
        self.btn_start.grid(row=0, column=0, padx=8)

        self.btn_stop = ttk.Button(btn_frame, text="断开连接", command=self.stop_tunnel, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=1, padx=8)

        # 日志框
        log_frame = ttk.Frame(self, style="Card.TFrame", padding=10)
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log = tk.Text(log_frame, height=14, bg="#0a192f", fg="white",
                           insertbackground="white", font=("Consolas", 10))
        self.log.pack(fill=tk.BOTH, expand=True)

        # 提示语
        disclaimer = ttk.Label(self, 
            text="此为免费软件，任何付费下载的版本都是骗局。\n仅限于原版免费发布，任何修改后收费传播的版本均与作者无关。",
            font=("Microsoft YaHei", 9), foreground="#4fc3f7", background="#0d1b2a", justify="center")
        disclaimer.pack(pady=5)

        # 许可证声明
        license_label = ttk.Label(self, 
            text="本软件使用 AGPLv3 许可证发布", 
            font=("Microsoft YaHei", 8), foreground="gray", background="#0d1b2a")
        license_label.pack(side="bottom", pady=5)

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
