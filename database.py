from pathlib import Path
import aiosqlite

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "education_bot.db"


async def create_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                username TEXT,
                name TEXT,
                phone TEXT,
                age INTEGER,
                location TEXT,
                subject TEXT,
                level TEXT,
                education_format TEXT,
                lesson_time TEXT,
                price INTEGER,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_application(
    telegram_id,
    username,
    name,
    phone,
    age,
    location,
    subject,
    level,
    education_format,
    lesson_time,
    price
):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            INSERT INTO applications (
                telegram_id,
                username,
                name,
                phone,
                age,
                location,
                subject,
                level,
                education_format,
                lesson_time,
                price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            telegram_id,
            username,
            name,
            phone,
            age,
            location,
            subject,
            level,
            education_format,
            lesson_time,
            price
        ))

        await db.commit()

        return cursor.lastrowid


async def update_application_status(application_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            UPDATE applications
            SET status = ?
            WHERE id = ?
        """, (
            status,
            application_id
        ))

        await db.commit()


async def get_applications():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                id,
                name,
                phone,
                age,
                location,
                subject,
                level,
                education_format,
                lesson_time,
                price,
                status,
                created_at
            FROM applications
            ORDER BY id DESC
        """)

        applications = await cursor.fetchall()

        return applications


async def get_applications_by_status(status):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                id,
                name,
                phone,
                age,
                location,
                subject,
                level,
                education_format,
                lesson_time,
                price,
                status,
                created_at
            FROM applications
            WHERE status = ?
            ORDER BY id DESC
        """, (status,))

        applications = await cursor.fetchall()

        return applications

async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT COUNT(*) FROM applications
        """)
        total = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE status = 'new'
        """)
        new = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE status = 'contacted'
        """)
        contacted = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE status = 'accepted'
        """)
        accepted = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE status = 'rejected'
        """)
        rejected = (await cursor.fetchone())[0]

        return {
            "total": total,
            "new": new,
            "contacted": contacted,
            "accepted": accepted,
            "rejected": rejected
        }