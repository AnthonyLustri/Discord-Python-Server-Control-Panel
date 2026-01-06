import discord
from discord.ext import commands
import aiohttp
import asyncio
import datetime
import pyautogui
import psutil
import pygetwindow as gw
import os
import subprocess
from zoneinfo import ZoneInfo
from rcon.source import Client
from discord import app_commands
from PIL import Image

# ==============================
# CONFIGURATION
# ==============================
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CONTROL_CHANNEL_ID = 000000000000000000  # replace with your control channel ID
LOG_CHANNEL_ID = 000000000000000000      # replace with your log channel ID
STEAM_API_KEY = "YOUR_STEAM_API_KEY"
ALLOWED_ROLES = ["Admin", "Moderator", "Server Manager"]
BANLIST_PATH = r"D:\asmdata\Servers\The Island\ShooterGame\Binaries\Win64\BanList.txt"

ASM_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# ==============================
# SERVER CONFIGURATIONS
# ==============================
# Use placeholder IPs (127.0.0.1) and fake profile IDs.
# Load real values from environment variables or a private config file in production.
ASM_SERVERS_ASE = [
    {"name": "The Island 🗿", "profile_id": "ase-11111111-1111-1111-1111-111111111111", "rcon_ip": "127.0.0.1", "rcon_port": 15513, "rcon_password": "RCON_PASSWORD_1"},
    {"name": "Scorched Earth 🔥", "profile_id": "ase-22222222-2222-2222-2222-222222222222", "rcon_ip": "127.0.0.1", "rcon_port": 15528, "rcon_password": "RCON_PASSWORD_1"},
    {"name": "Aberration 🧪", "profile_id": "ase-33333333-3333-3333-3333-333333333333", "rcon_ip": "127.0.0.1", "rcon_port": 15518, "rcon_password": "RCON_PASSWORD_2"},
    {"name": "Extinction ☄️", "profile_id": "ase-44444444-4444-4444-4444-444444444444", "rcon_ip": "127.0.0.1", "rcon_port": 11185, "rcon_password": "RCON_PASSWORD_3"},
    {"name": "Genesis: Part 1 🧬", "profile_id": "ase-55555555-5555-5555-5555-555555555555", "rcon_ip": "127.0.0.1", "rcon_port": 15543, "rcon_password": "RCON_PASSWORD_4"},
    {"name": "Genesis: Part 2 🚀", "profile_id": "ase-66666666-6666-6666-6666-666666666666", "rcon_ip": "127.0.0.1", "rcon_port": 15549, "rcon_password": "RCON_PASSWORD_5"},
    {"name": "Ragnarok ⚔️", "profile_id": "ase-77777777-7777-7777-7777-777777777777", "rcon_ip": "127.0.0.1", "rcon_port": 15533, "rcon_password": "RCON_PASSWORD_1"},
    {"name": "Valguero 🐺", "profile_id": "ase-88888888-8888-8888-8888-888888888888", "rcon_ip": "127.0.0.1", "rcon_port": 11180, "rcon_password": "RCON_PASSWORD_6"},
    {"name": "Crystal Isles 💎", "profile_id": "ase-99999999-9999-9999-9999-999999999999", "rcon_ip": "127.0.0.1", "rcon_port": 15538, "rcon_password": "RCON_PASSWORD_7"},
    {"name": "Lost Island 🦅", "profile_id": "ase-aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "rcon_ip": "127.0.0.1", "rcon_port": 15559, "rcon_password": "RCON_PASSWORD_8"},
    {"name": "Fjordur ❄️", "profile_id": "ase-bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "rcon_ip": "127.0.0.1", "rcon_port": 15574, "rcon_password": "RCON_PASSWORD_9"},
    {"name": "The Center 🌋", "profile_id": "ase-ccccccc3-cccc-cccc-cccc-cccccccccccc", "rcon_ip": "127.0.0.1", "rcon_port": 25523, "rcon_password": "RCON_PASSWORD_10"},
    {"name": "Aquatica 🌊", "profile_id": "ase-ddddddd4-dddd-dddd-dddd-dddddddddddd", "rcon_ip": "127.0.0.1", "rcon_port": 16120, "rcon_password": "RCON_PASSWORD_11"},
]

ASM_SERVERS_ASA = [
    {
        "name": "The Island 🗿",
        "profile_id": "asa-1111",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11115,
        "rcon_password": "RCON_PASSWORD_12",
        "log_path": r"G:\WindowsGSM\servers\1\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "Scorched Earth 🔥",
        "profile_id": "asa-2222",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11125,
        "rcon_password": "RCON_PASSWORD_13",
        "log_path": r"G:\WindowsGSM\servers\2\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "The Center 🌋",
        "profile_id": "asa-3333",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11120,
        "rcon_password": "RCON_PASSWORD_14",
        "log_path": r"G:\WindowsGSM\servers\4\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "Aberration 🧪",
        "profile_id": "asa-4444",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11135,
        "rcon_password": "RCON_PASSWORD_15",
        "log_path": r"G:\WindowsGSM\servers\6\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "Ragnarok ⚔️",
        "profile_id": "asa-5555",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11175,
        "rcon_password": "RCON_PASSWORD_16",
        "log_path": r"G:\WindowsGSM\servers\10\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "Extinction ☄️",
        "profile_id": "asa-6666",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11140,
        "rcon_password": "RCON_PASSWORD_17",
        "log_path": r"G:\WindowsGSM\servers\8\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
    {
        "name": "Valguero 🐺",
        "profile_id": "asa-7777",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 11145,
        "rcon_password": "RCON_PASSWORD_18",
        "log_path": r"G:\WindowsGSM\servers\13\serverfiles\ShooterGame\Saved\Logs\ShooterGame.log"
    },
]

PALWORLD_SERVER = [
    {
        "name": "MainWorld 🌍",
        "profile_id": "palworld-main-1",
        "rcon_ip": "127.0.0.1",
        "rcon_port": 8211,
        "rcon_password": "PALWORLD_RCON_PASSWORD"
    }
]

# ==============================
# BOT INITIALIZATION
# ==============================
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# UTILITIES
# ==============================
def now_est():
    try:
        return datetime.datetime.now(ZoneInfo("America/New_York"))
    except Exception:
        return datetime.datetime.utcnow()


async def log_admin_action(emoji, action, target, id_value, moderator):
    ch = bot.get_channel(LOG_CHANNEL_ID)
    if not ch:
        return
    embed = discord.Embed(title=f"{emoji} {action}", color=discord.Color.orange(), timestamp=now_est())
    embed.add_field(name="Target", value=target, inline=False)
    embed.add_field(name="Profile/SteamID", value=id_value, inline=False)
    embed.add_field(name="Moderator", value=moderator.mention, inline=False)
    await ch.send(embed=embed)


async def schedule_channel_cleanup(channel: discord.TextChannel, delay: int = 60):
    await asyncio.sleep(delay)
    try:
        async for msg in channel.history(limit=100):
            if msg.pinned or msg.author != bot.user:
                continue
            await msg.delete()
    except Exception as e:
        print(f"[CleanupError] {e}")

# ==============================
# CROSSCHAT RESTART HELPER
# ==============================
async def restart_crosschat(interaction: discord.Interaction):
    """Fully restarts CrossChat Evolved Bot on the server."""
    try:
        # Path to CrossChat executable (no sensitive user name)
        exe_path = r"C:\Path\To\CrosschatEvolvedBot\crosschatevolvedbot.exe"
        exe_dir = os.path.dirname(exe_path)

        subprocess.run(
            ["taskkill", "/f", "/im", "crosschatevolvedbot.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        await asyncio.sleep(1)

        cmd = f'start "" "{exe_path}"'
        subprocess.Popen(
            cmd,
            cwd=exe_dir,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        await interaction.response.send_message(
            "🔁 CrossChat Evolved Bot restarted successfully!",
            ephemeral=True
        )
        await schedule_channel_cleanup(interaction.channel)

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to restart CrossChat: `{e}`",
            ephemeral=True
        )

# ==============================
# ASM SNAPSHOT HELPER
# ==============================
async def take_asm_snapshot(interaction: discord.Interaction):
    """Captures only the Ark Server Manager window (even if minimized) and sends it to Discord."""
    try:
        window = None
        for w in gw.getWindowsWithTitle("ARK: Survival Evolved"):
            if "Server Manager" in w.title:
                window = w
                break

        if not window:
            await interaction.response.send_message(
                "❌ Could not find the ARK: Survival Evolved™ Server Manager window.",
                ephemeral=True
            )
            return

        if window.isMinimized:
            window.restore()
            await asyncio.sleep(1)

        window.activate()
        await asyncio.sleep(0.5)

        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        width, height = right - left, bottom - top

        img = pyautogui.screenshot(region=(left, top, width, height))

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, f"asm_snapshot_{timestamp}.png")
        img.save(img_path)

        await interaction.response.send_message(
            "📸 **ARK Server Manager Snapshot:**",
            file=discord.File(img_path)
        )
        await schedule_channel_cleanup(interaction.channel)

        os.remove(img_path)
        window.minimize()

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to capture ASM snapshot: `{e}`",
            ephemeral=True
        )

# ==============================
# ASM CONTROL VIA WEBHOOK
# ==============================
async def asm_send_via_webhook(content: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                ASM_WEBHOOK_URL,
                json={"content": content, "username": "Notification"}
            ) as resp:
                if resp.status not in (200, 204):
                    print(f"[ASM_WEBHOOK] Error HTTP {resp.status}")
                    return
                data = await resp.json() if resp.content_type == "application/json" else None

        if data and "id" in data and "channel_id" in data:
            await asyncio.sleep(1)
            msg_id = data["id"]
            channel_id = data["channel_id"]

            delete_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_id}"
            async with aiohttp.ClientSession() as session:
                await session.delete(delete_url)
    except Exception as e:
        print(f"[ASM_WEBHOOK ERROR] {e}")


async def asm_start_server(pid):
    await asm_send_via_webhook(f"!asmstart {pid}")


async def asm_stop_server(pid):
    await asm_send_via_webhook(f"!asmstop {pid}")


async def asm_restart_server(pid):
    await asm_send_via_webhook(f"!asmrestart {pid}")


async def asm_batch(action, servers, moderator):
    for s in servers:
        pid = s["profile_id"]
        name = s["name"]

        if action == "start":
            await asm_start_server(pid)
        elif action == "stop":
            await asm_stop_server(pid)
        elif action == "restart":
            await asm_restart_server(pid)

        await log_admin_action("⚙️", f"{action.title()} Command Sent", name, pid, moderator)
        await asyncio.sleep(5)

# ==============================
# WINDOWS GSM CONTROL VIA WEBHOOK
# ==============================
async def wgsm_send_via_webhook(content: str):
    """Send a WindowsGSM command silently via webhook."""
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                ASM_WEBHOOK_URL,
                json={"content": content, "username": "WindowsGSM Controller"}
            )
    except Exception as e:
        print(f"[WGSM_WEBHOOK ERROR] {e}")


async def wgsm_start_server(server_id):
    await wgsm_send_via_webhook(f"wgsm start {server_id}")


async def wgsm_stop_server(server_id):
    await wgsm_send_via_webhook(f"wgsm stop {server_id}")


async def wgsm_restart_server(server_id):
    await wgsm_send_via_webhook(f"wgsm restart {server_id}")


async def wgsm_update_server(server_id):
    await wgsm_send_via_webhook(f"wgsm update {server_id}")

# ==============================
# RCON / STEAM HELPERS
# ==============================
async def rcon_send(ip, port, password, cmd, timeout=6):
    def work():
        try:
            with Client(ip, port, passwd=password) as client:
                return client.run(cmd)
        except Exception as e:
            return f"RCON Error: {e}"

    try:
        return await asyncio.wait_for(asyncio.to_thread(work), timeout=timeout)
    except asyncio.TimeoutError:
        return "RCON Timeout"


async def rcon_ping(server):
    try:
        reader, writer = await asyncio.open_connection(server["rcon_ip"], server["rcon_port"])
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


async def steam_lookup(steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
    try:
        return data["response"]["players"][0]["personaname"]
    except Exception:
        return "Unknown Player"


async def is_palworld_online(process_name="PalServer-Win64-Shipping-Cmd.exe") -> bool:
    """Check if the Palworld server process is running."""
    try:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                return True
    except Exception as e:
        print(f"[PalworldCheck] {e}")
    return False


async def build_banlist_rows_from_file():
    if not os.path.exists(BANLIST_PATH):
        return ["❌ BanList.txt not found."]

    with open(BANLIST_PATH, "r") as f:
        steam_ids = [line.strip() for line in f if line.strip()]

    if not steam_ids:
        return ["✅ No banned players."]

    rows = []
    async with aiohttp.ClientSession() as session:
        for sid in steam_ids[:25]:
            try:
                async with session.get(
                    f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={sid}"
                ) as r:
                    data = await r.json()
                p = data.get("response", {}).get("players", [{}])[0]
                name = p.get("personaname", "Unknown")
                url = p.get("profileurl", f"https://steamcommunity.com/profiles/{sid}")
            except Exception:
                name = "Unknown"
                url = f"https://steamcommunity.com/profiles/{sid}"

            rows.append(f"[{name}]({url}) | `{sid}`")
            await asyncio.sleep(0.3)

    return rows


async def cluster_ban(steam_id):
    results = []
    for s in ASM_SERVERS_ASE:
        res = await rcon_send(s["rcon_ip"], s["rcon_port"], s["rcon_password"], f"banplayer {steam_id}")
        results.append((s["name"], "Success" if "Error" not in res else res))
    return results


async def cluster_unban(steam_id):
    results = []
    for s in ASM_SERVERS_ASE:
        res = await rcon_send(s["rcon_ip"], s["rcon_port"], s["rcon_password"], f"unbanplayer {steam_id}")
        results.append((s["name"], "Success" if "Error" not in res else res))
    return results


def read_asa_version_from_log(path: str) -> str:
    """Reads the ARK ASA version number from a server's ShooterGame.txt log."""
    try:
        if not os.path.exists(path):
            return "❌ No log"
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for line in reversed(lines[-500:]):
            if "ARK Version" in line:
                import re
                m = re.search(r"Version[:\s]+([\d\.]+)", line)
                if m:
                    return f"v{m.group(1)}"
        return "⚠️ Not found"
    except Exception:
        return "Error"

# ==============================
# DISCORD UI COMPONENTS
# ==============================
class ConfirmDeleteView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=20)
        self.channel = channel

    @discord.ui.button(label="🗑️ Confirm Delete", style=discord.ButtonStyle.success)
    async def confirm(self, i: discord.Interaction, _):
        await i.response.defer(ephemeral=True)
        deleted = 0
        async for msg in self.channel.history(limit=None):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.5)
            except Exception:
                continue

        await i.followup.send(
            f"🧹 Cleared **{deleted} messages** from {self.channel.mention}.",
            ephemeral=True
        )

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled.", ephemeral=True)

class RestartCrossChatButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔁 Restart CrossChat", style=discord.ButtonStyle.primary)

    async def callback(self, i: discord.Interaction):
        roles = [r.name for r in i.user.roles]
        if not any(r in ALLOWED_ROLES for r in roles):
            await i.response.send_message("❌ You don’t have permission to restart CrossChat.", ephemeral=True)
            return

        await restart_crosschat(i)

class ASMSnapshotButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📸 Take ASM Snapshot", style=discord.ButtonStyle.blurple)

    async def callback(self, i: discord.Interaction):
        roles = [r.name for r in i.user.roles]
        if not any(r in ALLOWED_ROLES for r in roles):
            await i.response.send_message(
                "❌ You don’t have permission to take a snapshot.",
                ephemeral=True
            )
            return

        await take_asm_snapshot(i)

class DeleteChannelButton(discord.ui.Button):
    last_used = 0

    def __init__(self):
        super().__init__(label="🗑️ Delete Messages", style=discord.ButtonStyle.success)

    async def callback(self, i: discord.Interaction):
        roles = [r.name for r in i.user.roles]
        if not any(r in ALLOWED_ROLES for r in roles):
            await i.response.send_message(
                "❌ You don't have permission to delete messages.",
                ephemeral=True
            )
            return

        now = asyncio.get_event_loop().time()
        if now - DeleteChannelButton.last_used < 10:
            await i.response.send_message(
                "⏳ Please wait 10 seconds before using this again.",
                ephemeral=True
            )
            return

        DeleteChannelButton.last_used = now
        await i.response.send_message(
            f"⚠️ Are you sure you want to delete **all messages** in {i.channel.mention}? "
            "This cannot be undone.",
            view=ConfirmDeleteView(i.channel),
            ephemeral=True
        )

class BanPlayerModal(discord.ui.Modal, title="🚫 Ban Player"):
    steam_id = discord.ui.TextInput(label="SteamID64", required=True)
    reason = discord.ui.TextInput(
        label="Reason for Ban (optional)",
        style=discord.TextStyle.paragraph,
        required=False,
        placeholder="Example: Toxic behavior, griefing, cheating..."
    )

    async def on_submit(self, i: discord.Interaction):
        sid = self.steam_id.value.strip()
        name = await steam_lookup(sid)
        reason_text = self.reason.value.strip() if self.reason.value else "No reason provided."

        await i.response.send_message(
            f"Ban **{name}** ({sid}) from all servers?\n📝 **Reason:** {reason_text}",
            view=ConfirmBanView(sid, name, reason_text),
            ephemeral=True
        )

class ConfirmBanView(discord.ui.View):
    def __init__(self, steam_id, steam_name, reason):
        super().__init__(timeout=30)
        self.steam_id = steam_id
        self.steam_name = steam_name
        self.reason = reason

    @discord.ui.button(label="🚫 Confirm Ban", style=discord.ButtonStyle.danger)
    async def confirm(self, i: discord.Interaction, _):
        await i.response.defer(ephemeral=True, thinking=True)
        results = await cluster_ban(self.steam_id)

        lines = [
            f"🔴 Banning **{self.steam_name}** (`{self.steam_id}`):",
            f"📝 **Reason:** {self.reason}\n"
        ]
        success = 0
        for server_name, res in results:
            if "Success" in res:
                lines.append(f"✅ {server_name}")
                success += 1
            else:
                lines.append(f"❌ {server_name} – {res}")
        lines.append(f"\nSummary: {success}/{len(results)} servers succeeded.")

        embed = discord.Embed(
            title="Cluster Ban Results",
            description="\n".join(lines),
            color=discord.Color.red()
        )

        await i.followup.send(embed=embed, ephemeral=True)
        await log_admin_action("🚫", f"Banned Player\n📝 Reason: {self.reason}", self.steam_name, self.steam_id, i.user)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled.", ephemeral=True)

class BanPlayerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🚫 Ban Player", style=discord.ButtonStyle.red)

    async def callback(self, i: discord.Interaction):
        await i.response.send_modal(BanPlayerModal())

class BanListButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📜 Ban List", style=discord.ButtonStyle.blurple)

    async def callback(self, i: discord.Interaction):
        rows = await build_banlist_rows_from_file()
        e = discord.Embed(title="🚫 Banned Players", description="\n".join(rows), color=discord.Color.blue())
        await i.response.send_message(embed=e, ephemeral=True)
        await schedule_channel_cleanup(i.channel)

class UnbanPlayerModal(discord.ui.Modal, title="✅ Unban Player"):
    steam_id = discord.ui.TextInput(label="SteamID64", required=True)

    async def on_submit(self, i: discord.Interaction):
        sid = self.steam_id.value.strip()
        name = await steam_lookup(sid)
        await i.response.send_message(
            f"Unban **{name}** ({sid})?",
            view=ConfirmUnbanView(sid, name),
            ephemeral=True
        )

class ConfirmUnbanView(discord.ui.View):
    def __init__(self, steam_id, steam_name):
        super().__init__(timeout=30)
        self.steam_id = steam_id
        self.steam_name = steam_name

    @discord.ui.button(label="✅ Confirm Unban", style=discord.ButtonStyle.success)
    async def confirm(self, i: discord.Interaction, _):
        await i.response.defer(ephemeral=True, thinking=True)
        results = await cluster_unban(self.steam_id)
        lines = [f"🟢 Unbanning **{self.steam_name}** (`{self.steam_id}`):\n"]
        success = 0
        for server_name, res in results:
            if "Success" in res:
                lines.append(f"✅ {server_name}")
                success += 1
            else:
                lines.append(f"❌ {server_name} – {res}\n")
        lines.append(f"\nSummary: {success}/{len(results)} servers succeeded.")
        embed = discord.Embed(
            title="Cluster Unban Results",
            description="\n".join(lines),
            color=discord.Color.green()
        )
        await i.followup.send(embed=embed, ephemeral=True)
        await log_admin_action("✅", "Unbanned Player", self.steam_name, self.steam_id, i.user)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled.", ephemeral=True)

class UnbanPlayerButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="✅ Unban Player", style=discord.ButtonStyle.success)

    async def callback(self, i: discord.Interaction):
        await i.response.send_modal(UnbanPlayerModal())

class ReturnToMenuButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="↩️ Return to Main Menu", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.edit_message(
                content="🎮 **ARK Master Control Panel** (Main Menu)",
                view=MainMenu()
            )
            await schedule_channel_cleanup(interaction.channel)
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Failed to return to main menu: `{e}`",
                ephemeral=True
            )

class ConfirmServerActionView(discord.ui.View):
    def __init__(self, server, action):
        super().__init__(timeout=20)
        self.server = server
        self.action = action

    @discord.ui.button(label="✅ Yes, Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, i: discord.Interaction, _):
        await i.response.defer(ephemeral=True, thinking=True)

        if self.action == "start":
            await asm_start_server(self.server["profile_id"])
            emoji, color = "🟢", discord.Color.green()
        elif self.action == "stop":
            await asm_stop_server(self.server["profile_id"])
            emoji, color = "🔴", discord.Color.red()
        else:
            await asm_restart_server(self.server["profile_id"])
            emoji, color = "🔁", discord.Color.blurple()

        await log_admin_action(emoji, f"{self.action.title()}ed Server", self.server["name"], self.server["profile_id"], i.user)

        embed = discord.Embed(
            title=f"{emoji} {self.action.title()} Command Sent",
            description=f"**{self.server['name']}** has been {self.action}ed successfully.",
            color=color
        )
        await i.followup.send(embed=embed, ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled server action.", ephemeral=True)

class MapControlView(discord.ui.View):
    def __init__(self, server):
        super().__init__(timeout=60)
        self.server = server

    @discord.ui.button(label="▶️ Start", style=discord.ButtonStyle.success)
    async def start(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **start** {self.server['name']}?",
            view=ConfirmServerActionView(self.server, "start"),
            ephemeral=True
        )

    @discord.ui.button(label="🔁 Restart", style=discord.ButtonStyle.primary)
    async def restart(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **restart** {self.server['name']}?",
            view=ConfirmServerActionView(self.server, "restart"),
            ephemeral=True
        )

    @discord.ui.button(label="⛔ Stop", style=discord.ButtonStyle.danger)
    async def stop(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **stop** {self.server['name']}?",
            view=ConfirmServerActionView(self.server, "stop"),
            ephemeral=True
        )

class WGSMMapControlView(discord.ui.View):
    def __init__(self, server):
        super().__init__(timeout=60)
        self.server = server

    @discord.ui.button(label="▶️ Start", style=discord.ButtonStyle.success)
    async def start(self, i: discord.Interaction, _):
        await wgsm_start_server(self.server["profile_id"])
        await i.response.send_message(f"Start sent for {self.server['name']}.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="🔁 Restart", style=discord.ButtonStyle.primary)
    async def restart(self, i: discord.Interaction, _):
        await wgsm_restart_server(self.server["profile_id"])
        await i.response.send_message(f"Restart sent for {self.server['name']}.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="⛔ Stop", style=discord.ButtonStyle.danger)
    async def stop(self, i: discord.Interaction, _):
        await wgsm_stop_server(self.server["profile_id"])
        await i.response.send_message(f"Stop sent for {self.server['name']}.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="⬆️ Update", style=discord.ButtonStyle.blurple)
    async def update(self, i: discord.Interaction, _):
        await wgsm_update_server(self.server["profile_id"])
        await i.response.send_message(f"Update sent for {self.server['name']}.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

class PalworldControlView(discord.ui.View):
    def __init__(self, server):
        super().__init__(timeout=60)
        self.server = server

    @discord.ui.button(label="▶️ Start", style=discord.ButtonStyle.success)
    async def start(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **start** {self.server['name']}?",
            view=ConfirmPalworldCommandView(self.server, "start"),
            ephemeral=True
        )

    @discord.ui.button(label="🔁 Restart", style=discord.ButtonStyle.primary)
    async def restart(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **restart** {self.server['name']}?",
            view=ConfirmPalworldCommandView(self.server, "restart"),
            ephemeral=True
        )

    @discord.ui.button(label="⬆️ Update", style=discord.ButtonStyle.blurple)
    async def update(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **update** {self.server['name']}?",
            view=ConfirmPalworldCommandView(self.server, "update"),
            ephemeral=True
        )

    @discord.ui.button(label="⛔ Stop", style=discord.ButtonStyle.danger)
    async def stop(self, i: discord.Interaction, _):
        await i.response.send_message(
            f"⚠️ Are you sure you want to **stop** {self.server['name']}?",
            view=ConfirmPalworldCommandView(self.server, "stop"),
            ephemeral=True
        )

class ConfirmPalworldCommandView(discord.ui.View):
    def __init__(self, server, action):
        super().__init__(timeout=20)
        self.server = server
        self.action = action

    @discord.ui.button(label="✅ Yes, Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, i: discord.Interaction, _):
        await i.response.defer(ephemeral=True, thinking=True)

        command_map = {
            "start": "wgsm start 3",
            "stop": "wgsm stop 3",
            "restart": "wgsm restart 3",
            "update": "wgsm update 3"
        }

        cmd = command_map.get(self.action)
        if not cmd:
            await i.followup.send(f"❌ Unknown action: {self.action}", ephemeral=True)
            return

        await asm_send_via_webhook(cmd)

        emoji = {
            "start": "🟢",
            "stop": "🔴",
            "restart": "🔁",
            "update": "⬆️"
        }.get(self.action, "⚙️")

        await log_admin_action(
            emoji,
            f"{self.action.title()}ed Palworld Server",
            self.server["name"],
            self.server["profile_id"],
            i.user
        )

        embed = discord.Embed(
            title=f"{emoji} Palworld {self.action.title()} Command Sent",
            description=f"Command `{cmd}` executed for **{self.server['name']}**.",
            color=discord.Color.blue()
        )
        await i.followup.send(embed=embed, ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled Palworld action.", ephemeral=True)

class ConfirmAllView(discord.ui.View):
    def __init__(self, action, servers):
        super().__init__(timeout=30)
        self.action = action
        self.servers = servers

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, i: discord.Interaction, _):
        await asm_batch(self.action, self.servers, i.user)
        await i.response.send_message(f"All servers {self.action} sent.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, i: discord.Interaction, _):
        await i.response.send_message("Cancelled.", ephemeral=True)
        await schedule_channel_cleanup(i.channel)

async def build_category_view(servers):
    if servers == PALWORLD_SERVER:
        statuses = [await is_palworld_online()]
    else:
        statuses = await asyncio.gather(*(rcon_ping(s) for s in servers))

    v = discord.ui.View(timeout=120)
    for s, is_up in zip(servers, statuses):
        icon = "🟢" if is_up else "🔴"

        if "log_path" in s:
            version = read_asa_version_from_log(s["log_path"])
            label_text = f"{icon} {s['name']} ({version})"
        else:
            label_text = f"{icon} {s['name']}"

        b = discord.ui.Button(label=label_text, style=discord.ButtonStyle.secondary)

        async def make_cb(server_cfg):
            async def inner(i: discord.Interaction):
                if server_cfg in PALWORLD_SERVER:
                    view = PalworldControlView(server_cfg)
                elif server_cfg in ASM_SERVERS_ASA:
                    view = WGSMMapControlView(server_cfg)
                else:
                    view = MapControlView(server_cfg)

                await i.response.send_message(
                    f"Controls for **{server_cfg['name']}**",
                    view=view,
                    ephemeral=True
                )
                await schedule_channel_cleanup(i.channel)
            return inner

        b.callback = await make_cb(s)
        v.add_item(b)

    v.add_item(BanPlayerButton())
    v.add_item(UnbanPlayerButton())
    v.add_item(BanListButton())
    v.add_item(ReturnToMenuButton())

    return v

class CategoryButton(discord.ui.Button):
    def __init__(self, label, servers):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.servers = servers

    async def callback(self, i: discord.Interaction):
        await i.response.send_message(
            f"🗺️ **{self.label} Servers:**",
            view=await build_category_view(self.servers),
            ephemeral=True
        )
        await schedule_channel_cleanup(i.channel)

class MainMenu(discord.ui.View):
    """Main control panel layout."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CategoryButton("🦖 ARK: Survival Evolved", ASM_SERVERS_ASE))
        self.add_item(CategoryButton("🦕 ARK: Survival Ascended", ASM_SERVERS_ASA))
        self.add_item(CategoryButton("🐉 Palworld", PALWORLD_SERVER))
        self.add_item(DeleteChannelButton())
        self.add_item(RestartCrossChatButton())
        self.add_item(ASMSnapshotButton())

# ==============================
# SLASH COMMAND + AUTO CLEANUP
# ==============================
async def auto_delete_message(msg: discord.Message, delay: int = 5):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass

@bot.tree.command(name="control", description="Open or refresh the ARK Master Control Panel")
@app_commands.checks.has_any_role(*ALLOWED_ROLES)
async def control_panel(interaction: discord.Interaction):
    if interaction.channel_id != CONTROL_CHANNEL_ID:
        await interaction.response.send_message(
            f"❌ Please use this command in <#{CONTROL_CHANNEL_ID}>.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=False)
    ch = interaction.channel
    existing = None
    async for m in ch.history(limit=25):
        if m.author == bot.user and "🎮" in m.content:
            existing = m
            break

    if existing:
        try:
            await existing.edit(content="🎮 **ARK Master Control Panel** (updated)", view=MainMenu())
            note = await interaction.followup.send("✅ Control panel refreshed.", ephemeral=False)
            asyncio.create_task(auto_delete_message(note, 5))
            return
        except Exception as e:
            print(f"[PanelEditError] {e}")

    await ch.send("🎮 **ARK Master Control Panel**", view=MainMenu())
    note = await interaction.followup.send("✅ Control panel created.", ephemeral=False)
    asyncio.create_task(auto_delete_message(note, 5))

# ==============================
# BOT STARTUP / CLEANUP
# ==============================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Slash sync failed: {e}")

    ch = bot.get_channel(CONTROL_CHANNEL_ID)
    if not ch:
        return
    async for m in ch.history(limit=25):
        if m.author == bot.user and "🎮" in m.content:
            try:
                await m.edit(content="🎮 **ARK Master Control Panel** (reloaded)", view=MainMenu())
            except Exception as e:
                print(f"[StartupEditError] {e}")
            break
    else:
        await ch.send("🎮 **ARK Master Control Panel Online**", view=MainMenu())

@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user or msg.channel.id != CONTROL_CHANNEL_ID:
        return
    cleanup_phrases = [
        "start request",
        "command complete",
        "server is shutting down",
        "server has started",
        "server is stopping",
        "wgsm start",
        "wgsm stop",
        "wgsm restart",
        "wgsm update",
        "windowsgsm"
    ]
    if any(k in msg.content.lower() for k in cleanup_phrases):
        await asyncio.sleep(30)
        try:
            await msg.delete()
        except Exception:
            pass
    await bot.process_commands(msg)

# ==============================
# AUTO-REFRESH MAIN CONTROL PANEL
# ==============================
async def auto_refresh_control_panel():
    """Keeps the control panel visible at all times and refreshes it every 5 minutes."""
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            channel = bot.get_channel(CONTROL_CHANNEL_ID)
            if not channel:
                print("[AutoRefresh] Control channel not found.")
                await asyncio.sleep(60)
                continue

            found_panel = False
            async for msg in channel.history(limit=10):
                if msg.author == bot.user and "🎮" in msg.content:
                    found_panel = True
                    try:
                        await msg.edit(
                            content="🎮 **ARK Master Control Panel** (auto-refreshed)",
                            view=MainMenu()
                        )
                        print("[AutoRefresh] Control panel refreshed.")
                    except Exception as e:
                        print(f"[AutoRefreshError] {e}")
                    break

            if not found_panel:
                try:
                    await channel.send("🎮 **ARK Master Control Panel** (recreated)", view=MainMenu())
                    print("[AutoRefresh] Control panel recreated.")
                except Exception as e:
                    print(f"[AutoRefreshRecreateError] {e}")

            await asyncio.sleep(300)

        except Exception as e:
            print(f"[AutoRefreshLoopError] {e}")
            await asyncio.sleep(60)

@bot.event
async def setup_hook():
    bot.loop.create_task(auto_refresh_control_panel())

@bot.event
async def on_message_delete(msg: discord.Message):
    if msg.channel.id == CONTROL_CHANNEL_ID and msg.author == bot.user and "🎮" in msg.content:
        ch = msg.channel
        await asyncio.sleep(2)
        await ch.send("🎮 **ARK Master Control Panel** (auto-restored)", view=MainMenu())
        print("[AutoRestore] Control panel recreated immediately after deletion.")

# ==============================
# RUN BOT
# ==============================
bot.run(TOKEN)
