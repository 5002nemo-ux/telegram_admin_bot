from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatPermissions
from database import add_warn, reset_warns, get_user_by_username, get_warn_count, get_user_by_id, get_settings
from locales import get_text
import re
from datetime import timedelta, datetime

router = Router()

async def get_lang(chat_id: int):
    settings = await get_settings(chat_id)
    return settings.get("language", "uz")

async def is_admin(message: Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]

async def get_target(message: Message, command_name: str, lang: str):
    # Returns (target_id, target_name, remaining_text)
    parts = message.text.split(maxsplit=1)
    text_args = parts[1] if len(parts) > 1 else ""
    
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, text_args
        
    if not text_args:
        await message.answer(get_text(lang, "format_error", command=command_name), parse_mode="HTML")
        return None, None, None

    # 1. Check for text mention
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention" and entity.user:
                mention_text = message.text[entity.offset:entity.offset+entity.length]
                remaining = text_args.replace(mention_text, "", 1).strip()
                return entity.user.id, entity.user.full_name, remaining

    args_parts = text_args.split(maxsplit=1)
    target_str = args_parts[0]
    remaining = args_parts[1] if len(args_parts) > 1 else ""

    # 2. Check if target is a numeric ID
    if target_str.isdigit():
        target_id = int(target_str)
        try:
            member = await message.bot.get_chat_member(message.chat.id, target_id)
            return target_id, member.user.full_name, remaining
        except:
            await message.answer(get_text(lang, "not_found_id", id=target_id), parse_mode="HTML")
            return None, None, None

    # 3. Check if target is a username
    if target_str.startswith('@'):
        user = await get_user_by_username(target_str)
        if user:
            return user['user_id'], user['full_name'], remaining
        else:
            await message.answer(get_text(lang, "not_found_username", username=target_str, command=command_name), parse_mode="HTML")
            return None, None, None
            
    await message.answer(get_text(lang, "format_error", command=command_name), parse_mode="HTML")
    return None, None, None

def parse_time_and_reason(text: str, lang: str):
    if not text:
        return None, get_text(lang, "reason_empty"), get_text(lang, "time_perm")
        
    args = text.strip()
    time_match = re.match(r'^(\d+)(m|h|d)\b', args)
    if time_match:
        amount = int(time_match.group(1))
        unit = time_match.group(2)
        reason = args[time_match.end():].strip() or get_text(lang, "reason_empty")
        
        if unit == 'm': delta = timedelta(minutes=amount)
        elif unit == 'h': delta = timedelta(hours=amount)
        else: delta = timedelta(days=amount)
            
        unit_names = {'m': get_text(lang, 'time_m'), 'h': get_text(lang, 'time_h'), 'd': get_text(lang, 'time_d')}
        return datetime.now() + delta, reason, f"{amount} {unit_names.get(unit, unit)}"
    else:
        return None, args or get_text(lang, "reason_empty"), get_text(lang, "time_perm")

@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if message.chat.type == "private": return
    if not await is_admin(message): return
    
    lang = await get_lang(message.chat.id)
    target_id, target_name, remaining_text = await get_target(message, "ban", lang)
    if not target_id: return
        
    until_date, reason, time_str = parse_time_and_reason(remaining_text, lang)
    
    try:
        await message.bot.ban_chat_member(message.chat.id, target_id, until_date=until_date)
        text = get_text(lang, "ban_success", target=f"<a href='tg://user?id={target_id}'>{target_name}</a>", admin=message.from_user.full_name, time=time_str, reason=reason)
        await message.answer(text, parse_mode="HTML")
    except Exception:
        await message.answer(get_text(lang, "ban_error"))

@router.message(Command("mute"))
async def cmd_mute(message: Message):
    if message.chat.type == "private": return
    if not await is_admin(message): return
    
    lang = await get_lang(message.chat.id)
    target_id, target_name, remaining_text = await get_target(message, "mute", lang)
    if not target_id: return
        
    until_date, reason, time_str = parse_time_and_reason(remaining_text, lang)
        
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, 
            target_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        text = get_text(lang, "mute_success", target=f"<a href='tg://user?id={target_id}'>{target_name}</a>", admin=message.from_user.full_name, time=time_str, reason=reason)
        await message.answer(text, parse_mode="HTML")
    except Exception:
        await message.answer(get_text(lang, "mute_error"))

@router.message(Command("unmute"))
async def cmd_unmute(message: Message):
    if message.chat.type == "private": return
    if not await is_admin(message): return
    
    lang = await get_lang(message.chat.id)
    target_id, target_name, _ = await get_target(message, "unmute", lang)
    if not target_id: return
    
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, 
            target_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True
            )
        )
        await message.answer(get_text(lang, "unmute_success", target=f"<a href='tg://user?id={target_id}'>{target_name}</a>"), parse_mode="HTML")
    except Exception:
        await message.answer(get_text(lang, "unmute_error"))

@router.message(Command("warn"))
async def cmd_warn(message: Message):
    if message.chat.type == "private": return
    if not await is_admin(message): return
    
    lang = await get_lang(message.chat.id)
    target_id, target_name, remaining_text = await get_target(message, "warn", lang)
    if not target_id: return
    
    reason = remaining_text.strip() if remaining_text else get_text(lang, "reason_empty")
    chat_id = message.chat.id
    
    try:
        member = await message.bot.get_chat_member(chat_id, target_id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            await message.answer(get_text(lang, "warn_admin_error"))
            return
    except:
        pass
    
    count = await add_warn(chat_id, target_id)
    
    if count >= 3:
        try:
            await message.bot.restrict_chat_member(
                chat_id, 
                target_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            text = get_text(lang, "warn_auto_mute", target=f"<a href='tg://user?id={target_id}'>{target_name}</a>", reason=reason)
            await message.answer(text, parse_mode="HTML")
            await reset_warns(chat_id, target_id)
        except Exception:
            await message.answer(get_text(lang, "mute_error"))
    else:
        text = get_text(lang, "warn_success", count=count, target=f"<a href='tg://user?id={target_id}'>{target_name}</a>", reason=reason, left=3-count)
        await message.answer(text, parse_mode="HTML")

@router.message(Command("info"))
async def cmd_info(message: Message):
    if message.chat.type == "private": return
    
    lang = await get_lang(message.chat.id)
    parts = message.text.split(maxsplit=1)
    if len(parts) == 1 and not message.reply_to_message:
        target_id = message.from_user.id
        target_name = message.from_user.full_name
    else:
        target_id, target_name, _ = await get_target(message, "info", lang)
        if not target_id: return
        
    try:
        member = await message.bot.get_chat_member(message.chat.id, target_id)
    except Exception:
        await message.answer(get_text(lang, "info_not_found"))
        return
        
    warns = await get_warn_count(message.chat.id, target_id)
    
    is_muted = False
    if member.status == ChatMemberStatus.RESTRICTED:
        if not member.can_send_messages:
            is_muted = True
            
    status_emoji = "👤"
    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        status_emoji = "👮‍♂️"
    elif is_muted:
        status_emoji = "🤐"
        
    db_user = await get_user_by_id(target_id)
    first_seen_str = get_text(lang, "unknown")
    if db_user and db_user.get("first_seen"):
        first_seen_str = db_user["first_seen"] + " (UTC)"
        
    mute_status_str = get_text(lang, "info_muted_yes") if is_muted else get_text(lang, "info_muted_no")
        
    text = get_text(lang, "info_text", emoji=status_emoji, target=f"<a href='tg://user?id={target_id}'>{target_name}</a>", id=target_id, warns=warns, mute_status=mute_status_str, first_seen=first_seen_str)
            
    await message.answer(text, parse_mode="HTML")
