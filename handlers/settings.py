from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus
from database import get_settings, update_setting, update_language
from locales import get_text

router = Router()

async def is_admin(message: Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]

def settings_keyboard(settings: dict, chat_id: int) -> InlineKeyboardMarkup:
    lang = settings.get("language", "uz")
    
    def icon(val): return get_text(lang, "settings_on") if val else get_text(lang, "settings_off")
    
    # Lang toggle: uz -> en -> ru -> uz
    next_lang = {'uz': 'en', 'en': 'ru', 'ru': 'uz'}
    current_lang = next_lang[lang]
    lang_flags = {'uz': '🇺🇿 UZ', 'en': '🇬🇧 EN', 'ru': '🇷🇺 RU'}
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{get_text(lang, 'settings_welcome')}: {icon(settings['welcome'])}", callback_data=f"set_welcome_{chat_id}_{int(not settings['welcome'])}")],
        [InlineKeyboardButton(text=f"{get_text(lang, 'settings_link')}: {icon(settings['anti_link'])}", callback_data=f"set_antilink_{chat_id}_{int(not settings['anti_link'])}")],
        [InlineKeyboardButton(text=f"{get_text(lang, 'settings_badword')}: {icon(settings['anti_bad_words'])}", callback_data=f"set_antibad_{chat_id}_{int(not settings['anti_bad_words'])}")],
        [InlineKeyboardButton(text=f"{get_text(lang, 'settings_lang')}: {lang_flags[lang]}", callback_data=f"set_lang_{chat_id}_{current_lang}")]
    ])
    return keyboard

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    if message.chat.type == "private":
        return
    
    if not await is_admin(message):
        return
    
    settings = await get_settings(message.chat.id)
    lang = settings.get("language", "uz")
    text = get_text(lang, "settings_title")
    await message.answer(text, reply_markup=settings_keyboard(settings, message.chat.id))

@router.callback_query(F.data.startswith("set_"))
async def process_setting_change(callback: CallbackQuery):
    parts = callback.data.split("_")
    action = parts[1]
    chat_id = int(parts[2])
    new_value = parts[3]
    
    member = await callback.bot.get_chat_member(chat_id, callback.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await callback.answer("Admin only!", show_alert=True)
        return

    if action == "lang":
        await update_language(chat_id, new_value)
    elif action == "welcome":
        await update_setting(chat_id, "welcome", bool(int(new_value)))
    elif action == "antilink":
        await update_setting(chat_id, "anti_link", bool(int(new_value)))
    elif action == "antibad":
        await update_setting(chat_id, "anti_bad_words", bool(int(new_value)))
        
    settings = await get_settings(chat_id)
    lang = settings.get("language", "uz")
    text = get_text(lang, "settings_title")
    
    await callback.message.edit_text(text, reply_markup=settings_keyboard(settings, chat_id))
    
    if action == "lang":
        await callback.answer(get_text(new_value, "lang_selected"))
    else:
        await callback.answer()
