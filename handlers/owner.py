from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import config
from database import get_all_groups
import asyncio

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.type != "private":
        return
        
    bot_info = await message.bot.me()
    text = (
        f"🤖 <b>Assalomu alaykum, {message.from_user.full_name}!</b>\n\n"
        "Men guruhlarni ortiqcha asabbuzarliklarsiz boshqarishga yordam beruvchi aqlli botman.\n\n"
        "<b>Mening vazifalarim:</b>\n"
        "🔗 Linklar va reklamalarni avtomatik o'chirish\n"
        "🤬 So'kinishlarni filtrlash\n"
        "🔇 Qoidabuzarlarni jazolash (Mute, Ban, Warn)\n"
        "🌐 Ko'p tilli qo'llab-quvvatlash (O'zbek, Rus, Ingliz)\n\n"
        "📞 <b>Murojaat uchun:</b> @eldorbek_muhiddinovich\n\n"
        "Meni guruhingizga qo'shing va to'liq <b>Admin huquqlarini</b> bering!"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Guruhga qo'shish", url=f"https://t.me/{bot_info.username}?startgroup=true")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(Command("id"))
async def cmd_id(message: Message):
    await message.answer(f"Sizning Telegram ID raqamingiz: <code>{message.from_user.id}</code>\nBuni config.py fayliga OWNER_ID sifatida kiriting.", parse_mode="HTML")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if message.from_user.id != config.OWNER_ID:
        await message.answer("Siz bot egasi emassiz! (config.py dagi OWNER_ID tekshiring)")
        return
        
    if not message.reply_to_message:
        await message.answer("Ushbu buyruqni tarqatmoqchi bo'lgan reklamangizga reply (javob) qilib yozing.\nMasalan: /broadcast")
        return
        
    groups = await get_all_groups()
    if not groups:
        await message.answer("Bot hali hech qaysi guruhga qo'shilmagan.")
        return
        
    success = 0
    await message.answer(f"Reklama {len(groups)} ta guruhga tarqatilmoqda...")
    for group_id in groups:
        try:
            await message.bot.copy_message(
                chat_id=group_id, 
                from_chat_id=message.chat.id, 
                message_id=message.reply_to_message.message_id
            )
            success += 1
            await asyncio.sleep(0.05) # Spam limitga tushmaslik uchun
        except Exception as e:
            # Guruhdan haydalgan bo'lishi mumkin
            pass
            
    await message.answer(f"✅ Tarqatish yakunlandi.\nMuvaffaqiyatli yetkazildi: {success} ta guruh.")
