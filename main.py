import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database import init_db
from handlers import settings, admin, filters, owner

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

async def main():
    # Ma'lumotlar bazasini ishga tushirish
    await init_db()
    
    # Render uchun soxta veb-serverni ishga tushirish
    asyncio.create_task(start_web_server())
    
    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Routerlarni (buyruqlarni) ulash. O'rnatish tartibi muhim!
    dp.include_router(owner.router)
    dp.include_router(settings.router)
    dp.include_router(admin.router)
    dp.include_router(filters.router)  # Filter eng oxirida turadi, xabarlarni tutib qolishi uchun
    
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish (Shaxsiy chatda)"),
        BotCommand(command="settings", description="Guruh sozlamalari (Adminlar)"),
        BotCommand(command="info", description="Foydalanuvchi ma'lumotlari"),
        BotCommand(command="ban", description="Foydalanuvchini guruhdan haydash"),
        BotCommand(command="mute", description="Yozishdan cheklash"),
        BotCommand(command="unmute", description="Mute'dan chiqarish"),
        BotCommand(command="warn", description="Ogohlantirish berish (3 marta = mute)"),
        BotCommand(command="broadcast", description="Barcha guruhlarga reklama tarqatish"),
        BotCommand(command="id", description="O'z ID raqamingizni ko'rish")
    ]
    await bot.set_my_commands(commands)
    
    # Botning bio va haqida qismini sozlash
    await bot.set_my_short_description("🤖 Guruhlar uchun aqlli anti-spam yordamchi bot.\n\n📞 Murojaat: @eldorbek_muhiddinovich")
    await bot.set_my_description("🤖 Guruh Yordamchisi - guruhingizni spam, linklar va so'kinishlardan tozalab beruvchi hamda qoidabuzarlarni jazolovchi mukammal bot!\n\nMeni guruhga qo'shing va to'liq admin huquqlarini bering.\n\n📞 Murojaat uchun: @eldorbek_muhiddinovich")
    
    # Botni ishga tushirish
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
