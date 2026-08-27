import os
import hashlib
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Global Error Handler (to handle spam and cooldowns)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏳ Cooldown Active",
            description=f"Easy there! Please wait a moment. Try again in **{round(error.retry_after, 1)} seconds**.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Argument",
            description="Hey buddy, you forgot to include the required details (like IP, URL, or text) with the command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
    else:
        print(f"Error encountered: {error}")

@bot.command(name="ping")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    """A simple ping command with professional embed."""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency is currently **{latency}ms**.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name="security")
@commands.cooldown(1, 5, commands.BucketType.user)
async def security_tip(ctx):
    """Provides a professional cybersecurity tip using embeds."""
    embed = discord.Embed(
        title="🔒 Cybersecurity Advisory",
        description="Always use strong, unique passwords and enable Multi-Factor Authentication (MFA) across all sensitive accounts.",
        color=discord.Color.blue()
    )
    embed.set_footer(text="CyberSecurityBot Intelligence Unit")
    await ctx.send(embed=embed)

@bot.command(name="lookup")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ip_lookup(ctx, ip_address: str):
    """Performs threat intelligence / geolocation lookup for an IP."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        
        if data["status"] == "success":
            embed = discord.Embed(
                title=f"🌐 Threat Intel: {ip_address}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Country", value=data.get("country", "N/A"), inline=True)
            embed.add_field(name="City", value=data.get("city", "N/A"), inline=True)
            embed.add_field(name="ISP", value=data.get("isp", "N/A"), inline=False)
            embed.add_field(name="Organization", value=data.get("org", "N/A"), inline=False)
            embed.set_footer(text="Data source: IP-API")
        else:
            embed = discord.Embed(
                title="❌ Lookup Failed",
                description=f"Could not retrieve information for IP: `{ip_address}`",
                color=discord.Color.red()
            )
            
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred while fetching data: {e}")

@bot.command(name="checkpass")
@commands.cooldown(1, 5, commands.BucketType.user)
async def check_password(ctx, *, password: str):
    """Checks the strength of a given password securely."""
    try:
        await ctx.message.delete()
    except:
        pass

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 8 and score >= 3:
        embed = discord.Embed(
            title="🔒 Password Strength: Strong",
            description=f"Hey {ctx.author.mention}, your password looks secure!",
            color=discord.Color.green()
        )
    elif length >= 6 and score >= 2:
        embed = discord.Embed(
            title="⚠️ Password Strength: Moderate",
            description=f"Hey {ctx.author.mention}, this password is okay, but can be stronger by adding numbers, capitals, or symbols.",
            color=discord.Color.orange()
        )
    else:
        embed = discord.Embed(
            title="❌ Password Strength: Weak",
            description=f"Hey {ctx.author.mention}, this password is too weak! Use at least 8 characters with a mix of uppercase, numbers, and symbols.",
            color=discord.Color.red()
        )

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}, I have sent the password security analysis to your Direct Messages (DMs) for privacy! 📩", delete_after=10)
    except Exception:
        await ctx.send("I couldn't send you a DM. Please enable your DMs!", embed=embed)

@bot.command(name="hash")
@commands.cooldown(1, 5, commands.BucketType.user)
async def generate_hash(ctx, *, text: str):
    """Generates SHA-256 and MD5 hashes for a given text securely."""
    try:
        await ctx.message.delete()
    except:
        pass

    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    md5_hash = hashlib.md5(text.encode()).hexdigest()

    embed = discord.Embed(
        title="🔐 Cryptographic Hash Generator",
        description=f"Requested by {ctx.author.mention} (Input text hidden for security)",
        color=discord.Color.purple()
    )
    embed.add_field(name="SHA-256 Hash", value=f"`{sha256_hash}`", inline=False)
    embed.add_field(name="MD5 Hash", value=f"`{md5_hash}`", inline=False)
    embed.set_footer(text="CyberSecurityBot Crypto Unit")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}, I have sent the hash results to your Direct Messages (DMs)! 📩", delete_after=10)
    except Exception:
        await ctx.send("I couldn't send you a DM. Please enable your DMs!", embed=embed)

@bot.command(name="checkurl")
@commands.cooldown(1, 5, commands.BucketType.user)
async def check_url(ctx, url: str):
    """Checks if a URL is safe or contains suspicious patterns."""
    try:
        await ctx.message.delete()
    except:
        pass

    suspicious_keywords = ["login", "verify", "update", "free", "account", "secure", "signin"]
    is_suspicious = any(keyword in url.lower() for keyword in suspicious_keywords)
    is_https = url.startswith("https://")

    if not is_https:
        embed = discord.Embed(
            title="⚠️ URL Safety Warning: Insecure Protocol",
            description=f"The URL `{url}` does not use HTTPS! It might be unencrypted.",
            color=discord.Color.orange()
        )
    elif is_suspicious:
        embed = discord.Embed(
            title="🚨 URL Safety Warning: Suspicious",
            description=f"The URL `{url}` contains common phishing keywords. Be careful before entering credentials!",
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="✅ URL Safety Check: Appears Safe",
            description=f"The URL `{url}` uses HTTPS and shows no immediate suspicious patterns.",
            color=discord.Color.green()
        )

    embed.set_footer(text="CyberSecurityBot URL Intelligence Unit")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}, I have sent the URL analysis to your DMs for safety! 📩", delete_after=10)
    except Exception:
        await ctx.send("I couldn't send you a DM. Please enable your DMs!", embed=embed)

@bot.command(name="portscan")
@commands.cooldown(1, 5, commands.BucketType.user)
async def port_scan(ctx, target: str):
    """Simulates a basic port scan on common network ports."""
    try:
        await ctx.message.delete()
    except:
        pass

    common_ports = {
        21: "FTP (File Transfer)",
        22: "SSH (Secure Shell)",
        80: "HTTP (Web Traffic)",
        443: "HTTPS (Secure Web Traffic)",
        3306: "MySQL Database",
        8080: "Alternative HTTP"
    }

    embed = discord.Embed(
        title=f"🛡️ Simulated Port Scan: {target}",
        description=f"Requested by {ctx.author.mention}. Scanning common ports...",
        color=discord.Color.blue()
    )

    for port, service in common_ports.items():
        status = "🟢 OPEN" if port in [80, 443, 22] else "🔴 CLOSED"
        embed.add_field(name=f"Port {port} ({service})", value=f"Status: {status}", inline=False)

    embed.set_footer(text="CyberSecurityBot Network Scanner Unit")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}, I have sent the port scan results to your DMs! 📩", delete_after=10)
    except Exception:
        await ctx.send("I couldn't send you a DM. Please enable your DMs!", embed=embed)

# Main entry point to run the bot
print("Starting bot...") 
try:
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN environment variable not found! Please check your .env file.")
    bot.run(TOKEN)
except Exception as e:
    print(f"An error occurred: {e}")