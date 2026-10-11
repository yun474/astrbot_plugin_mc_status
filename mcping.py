"""Minecraft Java 版 Server List Ping（1.7+），整合包服（Forge / NeoForge / Fabric）一样适用。"""

from __future__ import annotations

import asyncio
import json
import re
import struct
import time
from dataclasses import dataclass

import dns.asyncresolver
import dns.exception


DEFAULT_PORT = 25565
# 状态查询不挑客户端版本，服务端照样回自己的版本号
PROTOCOL_VERSION = 47
# 插件塞进 sample 里的提示行、开了隐身的玩家都用这个 UUID
NIL_UUID = "00000000-0000-0000-0000-000000000000"
FORMAT_CODE = re.compile(r"§.")


@dataclass
class ServerStatus:
    online: int
    max: int
    players: list[str]
    version: str
    latency: int


async def query(address: str, timeout: float) -> ServerStatus:
    return await asyncio.wait_for(_query(address), timeout)


async def _query(address: str) -> ServerStatus:
    host, port = await _resolve(address)
    reader, writer = await asyncio.open_connection(host, port)
    try:
        handshake = (
            _varint(PROTOCOL_VERSION)
            + _string(host)
            + struct.pack(">H", port)
            + _varint(1)
        )
        start = time.perf_counter()
        writer.write(_packet(0x00, handshake) + _packet(0x00))
        await writer.drain()
        await _read_varint(reader)
        latency = round((time.perf_counter() - start) * 1000)
        if await _read_varint(reader) != 0x00:
            raise ValueError("服务器回的不是状态包")
        data = await reader.readexactly(await _read_varint(reader))
    finally:
        writer.close()
    return _parse(json.loads(data), latency)


async def _resolve(address: str) -> tuple[str, int]:
    host, sep, port = address.rpartition(":")
    if sep:
        return host, int(port)
    try:
        answers = await dns.asyncresolver.resolve(f"_minecraft._tcp.{address}", "SRV")
    except dns.exception.DNSException:
        return address, DEFAULT_PORT
    record = min(answers, key=lambda r: (r.priority, -r.weight))
    return str(record.target).rstrip("."), record.port


def _parse(data: dict, latency: int) -> ServerStatus:
    players = data.get("players", {})
    names = [
        FORMAT_CODE.sub("", p.get("name", ""))
        for p in players.get("sample", [])
        if p.get("id") != NIL_UUID
    ]
    return ServerStatus(
        online=players.get("online", 0),
        max=players.get("max", 0),
        players=[n for n in names if n],
        version=FORMAT_CODE.sub("", data.get("version", {}).get("name", "")),
        latency=latency,
    )


def _varint(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if not value:
            out.append(byte)
            return bytes(out)
        out.append(byte | 0x80)


def _string(text: str) -> bytes:
    raw = text.encode()
    return _varint(len(raw)) + raw


def _packet(packet_id: int, payload: bytes = b"") -> bytes:
    body = _varint(packet_id) + payload
    return _varint(len(body)) + body


async def _read_varint(reader: asyncio.StreamReader) -> int:
    value = 0
    for shift in range(0, 35, 7):
        byte = (await reader.readexactly(1))[0]
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value
    raise ValueError("VarInt 太长")
