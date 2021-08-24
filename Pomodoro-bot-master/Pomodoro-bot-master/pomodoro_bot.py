import discord
from discord.ext import commands
import os
import platform
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from src.utils import get_expire_time

# Get token from ./token.txt
CURRENT_DIR_PATH = os.path.dirname(__file__)
if CURRENT_DIR_PATH == "":
    CURRENT_DIR_PATH = "."
if platform.system() == "Linux":
    CURRENT_DIR_PATH = CURRENT_DIR_PATH + "/"
elif platform.system() == "Windows":
    CURRENT_DIR_PATH = CURRENT_DIR_PATH + "\\"
t = open(CURRENT_DIR_PATH + "token.txt", "r", encoding="utf-8")
TOKEN = t.read().split()[0]

version = '1.0.0'
intents = discord.Intents.default()
intents.members = True
intents.presences = True
game = discord.Game(f"Pomodoro Bot {version}")
bot = commands.Bot(command_prefix='!', status=discord.Status.online,
                   activity=game, help_command=None, intents=intents)

sched = AsyncIOScheduler()


@bot.event
async def on_ready():
    print(" ---------------------")
    print(" POMODORO BOT on_ready")
    print(" ---------------------")
    sched.start()


@bot.command(name='pmdr_help')
async def send_help_message(ctx):
    """ Pomodoro bot help command
    Action:
        Send Pomodoro command help message
    """

    await ctx.channel.send(
        f"```css\n[Vahşi bota hoş geldiniz😎]\n - Çalışma komutu : !pmdr_start [çalışma_süresi] [mola_süresi]\n ex) !pmdr_start 25 "
        f"5\n -  Durdurma Komutu : !pmdr_stop```")


@bot.command(name='pmdr_start')
async def start_pomodoro_timer(ctx, çalışma_vakti: int, mola_vakti: int):
    """ Start pomodoro timer
    Action:
        Start mola_vakti timer after çalışma_vakti timer
    Args:
        çalışma_vakti : work timer (minute)
        mola_vakti : break timer after çalışma_vakti (minute)
    """

    if len(sched.get_jobs()) > 0:
        await ctx.channel.send(
            f"```css\n[❗️Vahşi bot iş başında❕]\n - Durdurma Komutu : !pmdr_stop```")
        return

    async def break_schedule(çalışma_vakti, mola_vakti):
        print('Enter break schedule')
        await ctx.channel.send(
            f"{ctx.author.mention}```css\n[🔥Ateş seni çağırıyor] 📢Hadi iş başına 🤓:)```")
        work_expire_time = get_expire_time(çalışma_vakti)
        sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[
                      çalışma_vakti, mola_vakti], misfire_grace_time=300)
        pass

    async def work_schedule(çalışma_vakti, mola_vakti):
        print('Enter work schedule')
        await ctx.channel.send(
            f"{ctx.author.mention}```css\n[🔔Mola zilleri çalıyor!] 📢Tembellik zamanı yeppaaaaa 🥳:)```")
        break_expire_time = get_expire_time(mola_vakti)
        sched.add_job(break_schedule, 'date', run_date=break_expire_time,
                      args=[çalışma_vakti, mola_vakti], misfire_grace_time=300)
        pass

    work_expire_time = get_expire_time(çalışma_vakti)
    sched.add_job(work_schedule, 'date', run_date=work_expire_time,
                  args=[çalışma_vakti, mola_vakti], misfire_grace_time=300)

    await ctx.channel.send(
        f"```css\n[Çalışma vakti {çalışma_vakti} dakika, Mola vakti {mola_vakti} dakika] Süre başladı📣\n - Durdurma Komutu : !pmdr_stop```")


@bot.command(name='pmdr_stop')
async def stop_pomodoro_timer(ctx):
    """ Stop pomodoro timer
    Action:
        Stop pomodoro timer
    """
    sched.remove_all_jobs()
    await ctx.channel.send(
        f"```css\nVahşi bot dinlenmeye çekildi😴.\n - Çalışma komutu : !pmdr_start [çalışma_süresü] [mola_süresi]```")


bot.run(TOKEN)