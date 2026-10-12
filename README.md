<div align="center">

# ⛏️ MC 服务器状态

**群里发一句 `/mc`，整合包服现在几个人在线一眼就知道。**

✨ [AstrBot](https://github.com/AstrBotDevs/AstrBot) · Java 版原生 Server List Ping · 整合包服直接可用 ✨

[![License: MIT](https://img.shields.io/badge/License-MIT-a3be8c.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-89b4fa.svg)](https://www.python.org/)
[![AstrBot 4.16+](https://img.shields.io/badge/AstrBot-4.16%2B-f2cd94.svg)](https://github.com/AstrBotDevs/AstrBot)
[![作者 yun474](https://img.shields.io/badge/作者-yun474-f5b7c7.svg)](https://github.com/yun474)

</div>

---

## ✨ 能做什么

- 用 Minecraft Java 版原生的 Server List Ping 协议查服，Forge / NeoForge / Fabric 整合包服、Velocity / BungeeCord 群组服都能查，服务端不用装任何东西。
- 显示在线人数、最大人数、版本，再加上服务器返回的玩家名，想看延迟也可以打开。
- 可以配多个服务器，同时查，一条消息全部列出来。
- 地址不写端口时会先查 `_minecraft._tcp` SRV 记录，跟游戏客户端一样。
- 机器人直连不到服务器也没关系，可以填个 HTTP 代理，比如内网的 Clash，让查询从代理那边走。

## 🚀 安装与使用

在 AstrBot 插件管理里用仓库地址 `https://github.com/yun474/astrbot_plugin_mc_status` 安装，需要 AstrBot 4.16 或更新版本。

在插件配置的「服务器列表」里加上服务器，然后在群里发（别名 `/mccx` 也行）：

```
/mc
```

回复长这样：

```
🟢 整合包服  17/50 人
版本：1.20.1
在线：Steve、Alex 等 17 人

🔴 测试服  连不上
```

## ⚙️ 配置说明

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| 服务器列表 | 空 | 一行一个，格式 `名称\|地址`，比如 `整合包服\|mc.example.com:25565`。不写名称就直接显示地址。 |
| 超时（秒） | 5 | 每个服务器最多等多久。 |
| HTTP 代理 | 空 | 留空就直连。走 Clash 就填它的局域网地址，比如 `http://192.168.1.10:7890`，Clash 要打开「允许局域网连接」。 |
| 显示延迟 | 关 | 在人数后面加上延迟，比如 `17/50 人  32ms`。走代理时是经过代理的往返时间。 |
| 显示玩家名 | 开 | 服务器最多只返回 12 个玩家名，开了隐身的不算，人多时会显示「等 N 人」。 |

## ❓ 常见问题

- **一直显示连不上**：先确认 AstrBot 所在机器能连到这个地址和端口，再检查服务端 `server.properties` 里的 `enable-status` 是不是 `true`。填了代理的话，再确认一下代理地址和端口有没有填对。具体的报错可以去 AstrBot 日志里看。
- **人数对但没玩家名**：有的服务端或插件会隐藏玩家列表，这时只显示人数。

## 📄 许可

[MIT](LICENSE)
