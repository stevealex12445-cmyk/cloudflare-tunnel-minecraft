import subprocess
import signal
import sys
print("输入域名")
domain = input("")
print("输入端口")
host = input("")
print("正在连接" + domain + host)

# 启动 cloudflared 隧道
proc = subprocess.Popen([
    r"cloudflared.exe",
    "access", "tcp",
    "--hostname", domain,
    "--listener", host
])

try:
    print("隧道已启动，本地监听:", host)
    # 在这里写你自己的逻辑，比如等待输入
    input("按回车键结束程序...\n")

finally:
    # 程序退出时结束隧道
    proc.terminate()   # 发送结束信号
    proc.wait()        # 等待进程退出
    print("隧道已关闭，程序结束。")