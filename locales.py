# -*- coding: utf-8 -*-

MESSAGES = {
    'uz': {
        'welcome': "👋 <b>Xush kelibsiz, {name}!</b>\n\nGuruhimiz qoidalariga rioya qilasiz degan umiddamiz. Yoqimli suhbat!",
        'welcome_bot': "🤖 <b>Assalomu alaykum!</b> Guruhni boshqarishga tayyorman.\n\n⚙️ Adminlar /settings buyrug'i orqali meni sozlashlari mumkin.\n❗️ Iltimos, menga guruhda to'liq <b>Admin huquqlarini</b> bering (xabarlarni o'chirish, ban qilish).",
        'anti_link': "⚠️ <b>{name}</b>, guruhda link tarqatish taqiqlangan!\nIltimos, qoidalarni buzmang.",
        'anti_bad_word': "🤬 <b>{name}</b>, iltimos guruhda so'kinmang!\nO'zaro hurmatni saqlang.",
        
        'ban_format': "⚠️ Ushbu buyruqni qoidabuzar xabariga reply (javob) qilib yozing yoki uning @nikneym yoki ID raqamini kiriting.\nMisol: <code>/ban @kimdir 1d qoidabuzarlik</code>",
        'ban_success': "⛔️ <b>Foydalanuvchi haydaldi!</b>\n\n👤 <b>Kim:</b> {target}\n👮‍♂️ <b>Admin:</b> {admin}\n⏳ <b>Muddat:</b> {time}\n📝 <b>Sabab:</b> {reason}",
        'ban_error': "❌ Xatolik: Men bu foydalanuvchini ban qila olmayman. Balki u admin bo'lishi mumkin.",
        
        'mute_success': "🤐 <b>Foydalanuvchi yozishdan cheklandi!</b>\n\n👤 <b>Kim:</b> {target}\n👮‍♂️ <b>Admin:</b> {admin}\n⏳ <b>Muddat:</b> {time}\n📝 <b>Sabab:</b> {reason}",
        'mute_error': "❌ Xatolik: Men bu foydalanuvchini mute qila olmayman.",
        
        'unmute_success': "🎙 <b>Afv etildi!</b>\n\n👤 {target} endi yana bemalol yoza oladi.",
        'unmute_error': "❌ Xatolik yuz berdi.",
        
        'warn_admin_error': "❌ Adminlarni ogohlantirib bo'lmaydi.",
        'warn_auto_mute': "🚫 <b>Avto-Mute!</b>\n\n👤 {target} <b>3 marta</b> ogohlantirildi va doimiy yozishdan cheklandi!\n📝 <b>Oxirgi sabab:</b> {reason}",
        'warn_success': "⚠️ <b>Ogohlantirish berildi! ({count}/3)</b>\n\n👤 <b>Kim:</b> {target}\n📝 <b>Sabab:</b> {reason}\n\n<i>❗️ Yana {left} marta ogohlantirish olsa, avtomatik Mute qilinadi.</i>",
        
        'info_not_found': "❌ Foydalanuvchini guruhdan topib bo'lmadi.",
        'info_text': "ℹ️ <b>Foydalanuvchi ma'lumoti</b>\n\n{emoji} <b>Foydalanuvchi:</b> {target}\n🆔 <b>ID:</b> <code>{id}</code>\n⚠️ <b>Ogohlantirishlar:</b> {warns} ta\n🔇 <b>Mute holati:</b> {mute_status}\n📅 <b>Birinchi marta ko'rilgan:</b> {first_seen}",
        'info_muted_yes': "Ha (Yozish taqiqlangan)",
        'info_muted_no': "Yo'q (Bemalol yoza oladi)",
        
        'settings_title': "⚙️ <b>Guruh sozlamalari</b>\n\nQuyidagi tugmalar orqali bot funksiyalarini yoqishingiz yoki o'chirishingiz mumkin:",
        'settings_welcome': "👋 Xush kelibsiz xabari",
        'settings_link': "🔗 Linklarni o'chirish",
        'settings_badword': "🤬 So'kinishlarni o'chirish",
        'settings_lang': "🌐 Tilni o'zgartirish",
        'settings_on': "✅ Yoqilgan",
        'settings_off': "❌ O'chirilgan",
        
        'lang_selected': "🇺🇿 Til O'zbek tiliga o'zgartirildi!",
        
        'not_found_id': "❌ <b>{id}</b> ID raqamiga ega foydalanuvchini guruhdan topa olmadim.",
        'not_found_username': "❌ <b>{username}</b> ismli foydalanuvchini bazamdan topa olmadim (u hali guruhda yozmagan).\nIltimos, uning ID raqamidan foydalaning.",
        'format_error': "⚠️ Iltimos, to'g'ri formatda kiriting.\nMisol: <code>/{command} @kimdir 1d qoidabuzarlik</code>",
        
        'time_m': "daqiqa",
        'time_h': "soat",
        'time_d': "kun",
        'time_perm': "Doimiy",
        'reason_empty': "Sabab ko'rsatilmadi",
        'unknown': "Noma'lum",
    },
    'en': {
        'welcome': "👋 <b>Welcome, {name}!</b>\n\nPlease follow the group rules. Enjoy your stay!",
        'welcome_bot': "🤖 <b>Hello!</b> I'm ready to manage the group.\n\n⚙️ Admins can configure me via the /settings command.\n❗️ Please grant me full <b>Admin rights</b> (delete messages, ban users).",
        'anti_link': "⚠️ <b>{name}</b>, sending links is forbidden in this group!\nPlease do not break the rules.",
        'anti_bad_word': "🤬 <b>{name}</b>, please do not use bad words in this group!\nKeep it respectful.",
        
        'ban_format': "⚠️ Reply to a message or enter the user's @username or ID to use this command.\nExample: <code>/ban @someone 1d breaking rules</code>",
        'ban_success': "⛔️ <b>User banned!</b>\n\n👤 <b>Who:</b> {target}\n👮‍♂️ <b>Admin:</b> {admin}\n⏳ <b>Duration:</b> {time}\n📝 <b>Reason:</b> {reason}",
        'ban_error': "❌ Error: I cannot ban this user. They might be an admin.",
        
        'mute_success': "🤐 <b>User muted!</b>\n\n👤 <b>Who:</b> {target}\n👮‍♂️ <b>Admin:</b> {admin}\n⏳ <b>Duration:</b> {time}\n📝 <b>Reason:</b> {reason}",
        'mute_error': "❌ Error: I cannot mute this user.",
        
        'unmute_success': "🎙 <b>Unmuted!</b>\n\n👤 {target} can now write messages again.",
        'unmute_error': "❌ An error occurred.",
        
        'warn_admin_error': "❌ You cannot warn an admin.",
        'warn_auto_mute': "🚫 <b>Auto-Mute!</b>\n\n👤 {target} received <b>3 warnings</b> and has been muted permanently!\n📝 <b>Last reason:</b> {reason}",
        'warn_success': "⚠️ <b>Warning given! ({count}/3)</b>\n\n👤 <b>Who:</b> {target}\n📝 <b>Reason:</b> {reason}\n\n<i>❗️ {left} more warnings will result in an auto-mute.</i>",
        
        'info_not_found': "❌ User not found in the group.",
        'info_text': "ℹ️ <b>User Info</b>\n\n{emoji} <b>User:</b> {target}\n🆔 <b>ID:</b> <code>{id}</code>\n⚠️ <b>Warnings:</b> {warns}\n🔇 <b>Muted:</b> {mute_status}\n📅 <b>First seen:</b> {first_seen}",
        'info_muted_yes': "Yes (Cannot write)",
        'info_muted_no': "No (Can write)",
        
        'settings_title': "⚙️ <b>Group Settings</b>\n\nToggle the bot features using the buttons below:",
        'settings_welcome': "👋 Welcome Message",
        'settings_link': "🔗 Anti-Link",
        'settings_badword': "🤬 Anti-Bad-Word",
        'settings_lang': "🌐 Change Language",
        'settings_on': "✅ On",
        'settings_off': "❌ Off",
        
        'lang_selected': "🇬🇧 Language changed to English!",
        
        'not_found_id': "❌ Cannot find user with ID <b>{id}</b> in the group.",
        'not_found_username': "❌ Cannot find user <b>{username}</b> in my database (they haven't written yet).\nPlease use their ID number instead.",
        'format_error': "⚠️ Please use the correct format.\nExample: <code>/{command} @someone 1d breaking rules</code>",
        
        'time_m': "minutes",
        'time_h': "hours",
        'time_d': "days",
        'time_perm': "Permanent",
        'reason_empty': "No reason provided",
        'unknown': "Unknown",
    },
    'ru': {
        'welcome': "👋 <b>Добро пожаловать, {name}!</b>\n\nНадеемся, вы будете соблюдать правила группы. Приятного общения!",
        'welcome_bot': "🤖 <b>Всем привет!</b> Я готов управлять группой.\n\n⚙️ Администраторы могут настроить меня через команду /settings.\n❗️ Пожалуйста, предоставьте мне полные <b>права Администратора</b> (удаление сообщений, бан).",
        'anti_link': "⚠️ <b>{name}</b>, отправка ссылок запрещена в этой группе!\nПожалуйста, не нарушайте правила.",
        'anti_bad_word': "🤬 <b>{name}</b>, пожалуйста, не используйте нецензурные слова!\nСохраняйте уважение.",
        
        'ban_format': "⚠️ Ответьте на сообщение пользователя или введите его @username или ID.\nПример: <code>/ban @someone 1d нарушение правил</code>",
        'ban_success': "⛔️ <b>Пользователь забанен!</b>\n\n👤 <b>Кто:</b> {target}\n👮‍♂️ <b>Админ:</b> {admin}\n⏳ <b>Срок:</b> {time}\n📝 <b>Причина:</b> {reason}",
        'ban_error': "❌ Ошибка: Я не могу забанить этого пользователя. Возможно, он администратор.",
        
        'mute_success': "🤐 <b>Пользователь ограничен!</b>\n\n👤 <b>Кто:</b> {target}\n👮‍♂️ <b>Админ:</b> {admin}\n⏳ <b>Срок:</b> {time}\n📝 <b>Причина:</b> {reason}",
        'mute_error': "❌ Ошибка: Я не могу ограничить этого пользователя.",
        
        'unmute_success': "🎙 <b>Прощен!</b>\n\n👤 {target} теперь снова может писать сообщения.",
        'unmute_error': "❌ Произошла ошибка.",
        
        'warn_admin_error': "❌ Администраторов нельзя предупреждать.",
        'warn_auto_mute': "🚫 <b>Авто-Мут!</b>\n\n👤 {target} получил <b>3 предупреждения</b> и был навсегда лишен права писать!\n📝 <b>Последняя причина:</b> {reason}",
        'warn_success': "⚠️ <b>Выдано предупреждение! ({count}/3)</b>\n\n👤 <b>Кто:</b> {target}\n📝 <b>Причина:</b> {reason}\n\n<i>❗️ Еще {left} предупреждения приведут к авто-муту.</i>",
        
        'info_not_found': "❌ Пользователь не найден в группе.",
        'info_text': "ℹ️ <b>Информация о пользователе</b>\n\n{emoji} <b>Пользователь:</b> {target}\n🆔 <b>ID:</b> <code>{id}</code>\n⚠️ <b>Предупреждения:</b> {warns}\n🔇 <b>Мут:</b> {mute_status}\n📅 <b>Впервые замечен:</b> {first_seen}",
        'info_muted_yes': "Да (Писать запрещено)",
        'info_muted_no': "Нет (Может писать)",
        
        'settings_title': "⚙️ <b>Настройки группы</b>\n\nВключите или отключите функции бота с помощью кнопок ниже:",
        'settings_welcome': "👋 Приветствие",
        'settings_link': "🔗 Удаление ссылок",
        'settings_badword': "🤬 Удаление мата",
        'settings_lang': "🌐 Изменить язык",
        'settings_on': "✅ Вкл",
        'settings_off': "❌ Выкл",
        
        'lang_selected': "🇷🇺 Язык изменен на русский!",
        
        'not_found_id': "❌ Не удалось найти пользователя с ID <b>{id}</b> в группе.",
        'not_found_username': "❌ Не удалось найти пользователя <b>{username}</b> в базе данных (он еще не писал).\nПожалуйста, используйте его ID.",
        'format_error': "⚠️ Пожалуйста, используйте правильный формат.\nПример: <code>/{command} @someone 1d нарушение</code>",
        
        'time_m': "минут",
        'time_h': "часов",
        'time_d': "дней",
        'time_perm': "Навсегда",
        'reason_empty': "Причина не указана",
        'unknown': "Неизвестно",
    }
}

BAD_WORDS_LISTS = {
    'uz': ["jinni", "ahmoq", "jalap", "qanjiq", "tupoy", "dalbayob", "haromi", "skatina", "padaras"],
    'en': ["fuck", "bitch", "shit", "asshole", "cunt", "motherfucker", "bastard"],
    'ru': ["блять", "сука", "пиздец", "хуй", "ебать", "пидор", "гандон", "шлюха"]
}

def get_text(lang_code: str, key: str, **kwargs) -> str:
    lang = lang_code if lang_code in MESSAGES else 'uz'
    text = MESSAGES[lang].get(key, MESSAGES['uz'].get(key, ""))
    if kwargs:
        return text.format(**kwargs)
    return text

def get_bad_words(lang_code: str) -> list:
    lang = lang_code if lang_code in BAD_WORDS_LISTS else 'uz'
    return BAD_WORDS_LISTS[lang]
