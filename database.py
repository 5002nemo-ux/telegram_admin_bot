import aiosqlite

DB_NAME = "bot_database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS group_settings (
                chat_id INTEGER PRIMARY KEY,
                welcome_enabled BOOLEAN DEFAULT 1,
                anti_link_enabled BOOLEAN DEFAULT 0,
                anti_bad_words_enabled BOOLEAN DEFAULT 1,
                language TEXT DEFAULT 'uz'
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_warnings (
                chat_id INTEGER,
                user_id INTEGER,
                count INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, user_id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                user_id INTEGER,
                full_name TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        try:
            await db.execute("ALTER TABLE users ADD COLUMN first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        except:
            pass
        try:
            await db.execute("ALTER TABLE group_settings ADD COLUMN language TEXT DEFAULT 'uz'")
        except:
            pass
            
        await db.commit()

async def get_settings(chat_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT welcome_enabled, anti_link_enabled, anti_bad_words_enabled, language FROM group_settings WHERE chat_id = ?", (chat_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "welcome": bool(row[0]),
                    "anti_link": bool(row[1]),
                    "anti_bad_words": bool(row[2]),
                    "language": row[3] if row[3] else "uz"
                }
            else:
                return {"welcome": True, "anti_link": True, "anti_bad_words": True, "language": "uz"}

async def update_setting(chat_id: int, setting: str, value: bool):
    mapping = {"welcome": "welcome_enabled", "anti_link": "anti_link_enabled", "anti_bad_words": "anti_bad_words_enabled"}
    col = mapping.get(setting, setting)
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(f'''
            INSERT INTO group_settings (chat_id, {col}) 
            VALUES (?, ?) 
            ON CONFLICT(chat_id) DO UPDATE SET {col} = excluded.{col}
        ''', (chat_id, value))
        await db.commit()

async def update_language(chat_id: int, language: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO group_settings (chat_id, language) 
            VALUES (?, ?) 
            ON CONFLICT(chat_id) DO UPDATE SET language = excluded.language
        ''', (chat_id, language))
        await db.commit()

async def get_all_groups():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT chat_id FROM group_settings") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def add_warn(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT count FROM user_warnings WHERE chat_id = ? AND user_id = ?", (chat_id, user_id)) as cursor:
            row = await cursor.fetchone()
            if row:
                new_count = row[0] + 1
                await db.execute("UPDATE user_warnings SET count = ? WHERE chat_id = ? AND user_id = ?", (new_count, chat_id, user_id))
            else:
                new_count = 1
                await db.execute("INSERT INTO user_warnings (chat_id, user_id, count) VALUES (?, ?, ?)", (chat_id, user_id, new_count))
            await db.commit()
            return new_count

async def reset_warns(chat_id: int, user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM user_warnings WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
        await db.commit()

async def get_warn_count(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT count FROM user_warnings WHERE chat_id = ? AND user_id = ?", (chat_id, user_id)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def save_user(user_id: int, username: str, full_name: str):
    if not username: return
    async with aiosqlite.connect(DB_NAME) as db:
        username = username.lower()
        # Ensure we don't overwrite first_seen if it already exists
        async with db.execute("SELECT user_id FROM users WHERE username = ?", (username,)) as cursor:
            exists = await cursor.fetchone()
            if not exists:
                await db.execute("INSERT INTO users (username, user_id, full_name) VALUES (?, ?, ?)", (username, user_id, full_name))
            else:
                await db.execute("UPDATE users SET user_id = ?, full_name = ? WHERE username = ?", (user_id, full_name, username))
        await db.commit()

async def get_user_by_username(username: str):
    username = username.lower().replace("@", "")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, full_name, first_seen FROM users WHERE username = ?", (username,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"user_id": row[0], "full_name": row[1], "first_seen": row[2]}
            return None

async def get_user_by_id(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, full_name, first_seen FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"user_id": row[0], "full_name": row[1], "first_seen": row[2]}
            return None
