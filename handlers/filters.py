from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
import re
from database import get_settings, save_user
from locales import get_text, get_bad_words

router = Router()

@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def filter_messages(message: Message):
    # Barcha yozganlarni bazaga saqlash
    if message.from_user and message.from_user.username:
        await save_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    settings = await get_settings(message.chat.id)
    lang = settings.get("language", "uz")

    # Yangi a'zolar qo'shilganda
    if message.new_chat_members:
        if settings["welcome"]:
            for new_member in message.new_chat_members:
                if new_member.id == message.bot.id:
                    await message.answer(get_text(lang, "welcome_bot"), parse_mode="HTML")
                    continue
                await message.answer(get_text(lang, "welcome", name=f"<a href='tg://user?id={new_member.id}'>{new_member.full_name}</a>"), parse_mode="HTML")
        return # Qolgan tekshiruvlar kerak emas

    if not message.text and not message.caption:
        return
        
    # Adminlarni, anonim adminlarni va guruhga ulangan kanal xabarlarini tekshirmaymiz
    try:
        if message.sender_chat and message.sender_chat.id == message.chat.id:
            return
        if getattr(message, "is_automatic_forward", False):
            return
            
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in ['creator', 'administrator']:
            return
    except:
        pass

    text = (message.text or message.caption).lower()

    # 1. Anti-link tekshiruvi
    if settings["anti_link"]:
        if "http://" in text or "https://" in text or "t.me/" in text or ".com" in text:
            await message.delete()
            await message.answer(get_text(lang, "anti_link", name=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"), parse_mode="HTML")
            return
            
    # 2. Anti-bad words tekshiruvi
    if settings["anti_bad_words"]:
        bad_words = get_bad_words(lang)
        for word in bad_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                await message.delete()
                await message.answer(get_text(lang, "anti_bad_word", name=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"), parse_mode="HTML")
                return
