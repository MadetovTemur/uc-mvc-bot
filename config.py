import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    SUPER_ADMIN_ID: int = int(os.getenv("SUPER_ADMIN_ID", "0") or "0")
    DB_PATH: str = os.getenv("DB_PATH", "shop.db")
    SUPPORT_CONTACT: str = os.getenv("SUPPORT_CONTACT", "@admin")

    # Стартовые цены, которые заносятся в БД при первом запуске бота.
    # Дальше все изменения цен делаются админом через бота (в БД),
    # эти значения больше не используются.
    DEFAULT_UC_PRICES: dict = field(default_factory=lambda: {
        60: 15000,
        120: 29000,
        180: 43000,
        355: 82000,
        420: 96000,
        720: 160000,
        1072: 235000,
        1440: 310000,
        1950: 415000,
        2670: 560000,
        3025: 630000,
    })


config = Config()
