import aiosqlite
import config

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Book:
    id: int
    ordering: int
    created_at: datetime
    title: str
    author: str
    book_state: datetime
    read_start: datetime
    state: str
    host: str


async def get_all_books() -> list[Book]:
    all_books = []
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as connection:
        async with connection.execute('SELECT * FROM book') as cursor:
            async for row in cursor:
                book = Book(
                    id=row[0],
                    created_at=row[1],
                    title=row[2],
                    author=row[3],
                    state=row[4],
                    ordering=row[5],
                    book_state=row[6],
                    read_start=row[7],
                    host=row[8]
                )
                all_books.append(book)
    return all_books
