import subprocess
import signal
import sys
print("输入域名/Enter domain")
domain = input("")
print("输入端口/Enter host")
host = input("")
print("正在连接/“Connecting…" + domain + host)
proc = subprocess.Popen([
    r"cloudflared.exe",
    "access", "tcp",
    "--hostname", domain,
    "--listener", "127.0.0.1:" + host
])
try:
    print("隧道已启动，本地监听:", host)
    input("按回车键结束程序...\n")
finally:
    proc.terminate() 
    proc.wait() 
    print("隧道已关闭，程序结束。")