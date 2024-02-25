import aiosqlite
import config

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    created_at: datetime
    read_start: datetime
    read_finish: datetime
    ordering: int
    state: str
    host: str


async def get_all_books() -> list[Book]:
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
                SELECT
                    id,
                    title,
                    author,
                    book_state,
                    created_at,
                    ordering,
                    read_start,
                    read_finish,
                    host
                FROM book
                """)
        rows = await cursor.fetchall()
        all_books = [Book(
                        id=row['id'],
                        title=row['title'],
                        author=row['author'],
                        state=row['book_state'],
                        created_at=row['created_at'],
                        ordering=row['ordering'],
                        read_start=row['read_start'],
                        read_finish=row['read_finish'],
                        host=row['host']
                    ) for row in rows]
    return all_books


async def get_current_book() -> Book | None:
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""SELECT * FROM book WHERE book_state = 'reading'""")
        item = await cursor.fetchone()
        if item:
            return Book(
                id=item['id'],
                title=item['title'],
                author=item['author'],
                state=item['book_state'],
                created_at=item['created_at'],
                ordering=item['ordering'],
                read_start=item['read_start'],
                read_finish=item['read_finish'],
                host=item['host'])
