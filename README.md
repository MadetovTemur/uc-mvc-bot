# UC Shop Bot (PUBG Mobile UC) — aiogram 3

Telegram-бот для продажи UC (PUBG Mobile) с ручным подтверждением платежей
администратором. Полностью переписан с MVP до "товарного" вида:
SQLite-база, роли user/admin/super_admin, лог каждого действия
пользователя, управление ценами и админами через бота, uz/ru.

## Архитектура

```
uc_shop_bot/
├── bot.py                     # точка входа
├── config.py                  # чтение .env
├── requirements.txt
├── .env.example
├── database/
│   ├── models.py               # SQLAlchemy-модели (User, Price, Order, ActionLog)
│   ├── db.py                   # engine/session (SQLite, aiosqlite, async)
│   └── requests.py             # весь доступ к БД (CRUD)
├── handlers/
│   ├── common.py                # /start, /cancel, выбор языка
│   ├── user.py                   # цены, покупка UC (FSM), список заказов, "о нас"
│   └── admin.py                  # заявки, цены, админы, статистика
├── keyboards/
│   ├── user_kb.py
│   └── admin_kb.py
├── states/states.py             # FSM-состояния (покупка, админ-формы)
├── middlewares/
│   ├── db_middleware.py          # сессия БД + текущий пользователь в data
│   └── logging_middleware.py     # пишет каждое действие в БД (action_logs) + bot.log
├── filters/admin_filters.py     # IsAdmin / IsSuperAdmin
├── locales/translations.py      # словари uz/ru + функция t(lang, key, **kwargs)
└── utils/logger.py
```

## Модель данных (SQLite)

- **users** — `telegram_id`, `username`, `full_name`, `language` (uz/ru),
  `role` (`user` / `admin` / `super_admin`), `is_blocked`, `created_at`.
- **prices** — `uc_amount`, `price` (сум), `is_active`, `sort_order`.
  Начальные значения из `config.DEFAULT_UC_PRICES` заносятся один раз при
  первом запуске (`ensure_default_prices`), дальше всё редактируется
  админом через бота и хранится только в БД.
- **orders** — `user_id`, `uc_amount`, `price`, `pubg_id`,
  `receipt_file_id` (file_id чека в Telegram), `status`
  (`pending` → `approved` / `rejected` / `cancelled`), `admin_id`,
  `admin_comment`, `created_at`, `updated_at`.
- **action_logs** — `telegram_id`, `action` (`message` / `callback`),
  `details` (текст сообщения или callback_data), `created_at`. Пишется
  через `ActionLoggingMiddleware` на **каждое** сообщение и нажатие
  кнопки — это и есть трекинг "каждого движения пользователя".

## Роли и админка

- Первый супер-админ назначается через `.env` (`SUPER_ADMIN_ID`) — когда
  человек с этим Telegram ID нажимает `/start`, ему присваивается роль
  `super_admin`.
- Супер-админ может назначать/снимать обычных админов прямо в боте
  (раздел «👤 Adminlarni boshqarish» / «Управление админами» → добавить
  по Telegram ID). Обычные админы админов назначать не могут.
- Админы видят отдельное меню (кнопки "Kutilayotgan buyurtmalar",
  "Narxlarni boshqarish", "Adminlarni boshqarish", "Statistika") вместо
  пользовательского.

## Логика покупки (FSM в `handlers/user.py`)

1. «UC xarid qilish» → бот показывает актуальные суммы UC из БД.
2. Пользователь выбирает сумму → вводит PUBG Mobile Global ID
   (валидируется regex'ом `^\d{5,15}$`).
3. Бот показывает итог заказа и просит прислать скриншот чека.
4. После получения фото создаётся `Order` со статусом `pending`, и
   **всем админам** уходит фото чека с карточкой заказа и кнопками
   ✅ Подтвердить / ❌ Отклонить.
5. Админ подтверждает → пользователю уходит уведомление "UC отправлены".
   Само отправление UC остаётся ручной операцией админа (как и было в
   MVP) — бот только фиксирует статус и уведомляет.
6. Админ отклоняет → бот просит ввести причину и присылает её
   пользователю.

## Установка на Ubuntu 22

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip

cd /opt
sudo git clone <ваш-репозиторий> uc_shop_bot   # или просто скопируйте папку
cd uc_shop_bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env     # укажите BOT_TOKEN и SUPER_ADMIN_ID

python3 bot.py
```

### Запуск как systemd-сервис (чтобы бот жил постоянно)

Создайте `/etc/systemd/system/uc-shop-bot.service`:

```ini
[Unit]
Description=UC Shop Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/uc_shop_bot
ExecStart=/opt/uc_shop_bot/venv/bin/python3 bot.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now uc-shop-bot
sudo systemctl status uc-shop-bot
journalctl -u uc-shop-bot -f
```

## Что дальше можно докрутить (не входит в текущую версию)

- Пагинация списка "Kutilayotgan buyurtmalar", если заявок станет много.
- Рассылка сообщений всем пользователям (broadcast) из админки.
- Блокировка пользователей (`is_blocked` уже есть в модели, фильтр под
  неё пока не подключен).
- Интеграция с платёжным провайдером вместо ручной проверки чека.
- Алембик-миграции, если структура БД будет часто меняться (сейчас
  таблицы создаются автоматически через `Base.metadata.create_all`).

## Примечание по проверке

Код проверен на синтаксис (`python3 -m py_compile`) и на соответствие
ключей переводов между `uz` и `ru`. Живой прогон с реальным токеном
Telegram здесь не выполнялся (нет сети), поэтому после установки
проверьте базовый сценарий вручную: `/start` → выбор языка → покупка →
подтверждение чека → появление заявки у админа → подтверждение/отклонение.
