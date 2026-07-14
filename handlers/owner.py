from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import config
from database import get_all_groups
import asyncio

router = Router()

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
