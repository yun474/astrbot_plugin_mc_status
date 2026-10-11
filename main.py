from __future__ import annotations

import asyncio

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .mcping import ServerStatus, query


class McStatusPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.command("mc", alias={"mccx"})
    async def mc(self, event: AstrMessageEvent):
        """查询我的世界服务器在线人数"""
        servers = [_split_entry(s) for s in self.config.get("servers", []) if s.strip()]
        if not servers:
            yield event.plain_result("还没配置服务器，去插件配置里加一个吧")
            return

        timeout = self.config.get("timeout", 5)
        results = await asyncio.gather(
            *(query(address, timeout) for _, address in servers),
            return_exceptions=True,
        )
        blocks = []
        for (name, address), result in zip(servers, results):
            if isinstance(result, BaseException):
                logger.warning(f"[mc_status] 查询 {address} 失败: {result!r}")
                blocks.append(f"🔴 {name}  连不上")
            else:
                blocks.append(self._format(name, result))
        yield event.plain_result("\n\n".join(blocks))

    def _format(self, name: str, status: ServerStatus) -> str:
        lines = [f"🟢 {name}  {status.online}/{status.max} 人  {status.latency}ms"]
        if status.version:
            lines.append(f"版本：{status.version}")
        if self.config.get("show_players", True) and status.players:
            players = "、".join(status.players)
            if status.online > len(status.players):
                players += f" 等 {status.online} 人"
            lines.append(f"在线：{players}")
        return "\n".join(lines)


def _split_entry(entry: str) -> tuple[str, str]:
    name, sep, address = entry.strip().partition("|")
    if not sep:
        return name, name
    return name.strip(), address.strip()
