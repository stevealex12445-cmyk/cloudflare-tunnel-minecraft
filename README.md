# CF 隧道 Minecraft 联机客户端

⚠️ 注意  
本工具仅作为 **客户端连接器** 使用，需要依赖已经配置好的 **Cloudflare Tunnel 服务端**。  
它不会自动创建或配置隧道，请先在服务端完成 Cloudflare Tunnel 的配置，再使用本工具进行连接。  

⚠️ 注意  
本工具目前仅支持通过 **TCP 协议** 连接至对端的 **25565 端口**（Minecraft 默认端口）。  
其他协议或端口暂不支持。  

## 前置依赖

本工具需要依赖 [cloudflared](https://github.com/cloudflare/cloudflared/releases) （Cloudflare 官方提供的隧道客户端）。

请根据你的系统下载对应版本并安装：
- Windows: `cloudflared-windows-amd64.exe`

本项目是一个 **客户端工具**，用于通过 **Cloudflare Tunnel** 建立隧道连接，从而实现 **Minecraft 服务器的多人联机**。  

⚠️ 注意事项：
- 本工具仅负责连接，不具备端口映射功能。  
- 由于 Cloudflare Tunnel 的特性，**延迟极高**，仅适合实验性或临时使用，不推荐长期部署。  

## 功能特点
- 作为客户端接入 Cloudflare Tunnel  
- 支持 Minecraft 联机连接  
- 轻量、易用  
- **由 AI 辅助编写与改进**  

## 使用方法
1. 配置好 Cloudflare Tunnel 的凭据。  
2. 运行客户端以建立隧道连接。  
3. 使用隧道连接加入 Minecraft 服务器。  

## 许可证
本项目基于 [AGPLv3](LICENSE) 协议开源。  
任何修改或衍生版本在提供网络服务时，必须同样以 AGPLv3 协议开源。  

## 发布记录
2025.9.27 0.9测试版
更新说明：无
2025.9.28 1.00正式版
更新说明：变得好看了（水一个正式版罢了）
2025.9.28
更新说明：删除了v0.9beta版，因为错误的使用了微软雅黑字体，修改较为繁琐。此外，v1.00已经使用思源黑体
