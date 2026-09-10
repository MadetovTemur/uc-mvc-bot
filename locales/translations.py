TRANSLATIONS: dict[str, dict[str, str]] = {
    "uz": {
        "welcome": "Salom, {name}! Botdan foydalanish uchun tugmalardan foydalaning 👇",
        "choose_language": "Tilni tanlang / Выберите язык:",
        "language_set": "✅ Til o'zbek tiliga o'rnatildi",
        "menu_prices": "💹 UC narxlari",
        "menu_buy": "♻️ UC xarid qilish",
        "menu_orders": "🧮 Orderlar ro'yxati",
        "menu_about": "👥 Biz xaqimizda",
        "menu_language": "🌐 Til / Язык",
        "prices_title": "📊 Joriy UC narxlari:\n\n",
        "price_line": "🔹 {amount} UC — {price} so'm\n",
        "choose_uc_amount": "Kerakli UC miqdorini tanlang:",
        "cancel_hint": "\nBekor qilish uchun buyruq: /cancel",
        "enter_pubg_id": "PUBG Mobile Global ID kiriting:",
        "invalid_pubg_id": "❌ ID noto'g'ri. Faqat raqamlardan iborat bo'lishi kerak (5-15 ta raqam). Qaytadan kiriting:",
        "confirm_order": (
            "🧾 Buyurtma ma'lumotlari:\n\n"
            "UC miqdori: {amount} UC\n"
            "Narxi: {price} so'm\n"
            "PUBG ID: {pubg_id}\n\n"
            "To'lovni amalga oshirib, chekni (screenshot) yuboring."
        ),
        "send_receipt": "📎 To'lov chekini (screenshot) yuboring.",
        "not_a_photo": "❌ Chek screenshot (rasm) ko'rinishida bo'lishi kerak. Qaytadan yuboring:",
        "order_created": (
            "✅ Buyurtmangiz qabul qilindi!\n\n"
            "Buyurtma raqami: #{order_id}\n"
            "Holati: ⏳ Ko'rib chiqilmoqda\n\n"
            "Admin tasdiqlagach sizga xabar beriladi."
        ),
        "cancelled": "❌ Amal bekor qilindi.",
        "nothing_to_cancel": "Bekor qilinadigan amal yo'q.",
        "orders_empty": "Sizda hali buyurtmalar yo'q.",
        "orders_stats": (
            "📊 Sizning statistikangiz:\n\n"
            "✅ Tasdiqlangan: {approved} ta\n"
            "⏳ Kutilmoqda: {pending} ta\n"
            "❌ Bekor/rad etilgan: {rejected_cancelled} ta"
        ),
        "order_status_pending": "⏳ Ko'rib chiqilmoqda",
        "order_status_approved": "✅ Tasdiqlangan",
        "order_status_rejected": "❌ Rad etilgan",
        "order_status_cancelled": "❌ Bekor qilingan",
        "order_item": "#{id} | {amount} UC | {price} so'm | {status}",
        "about_us": (
            "👥 Biz haqimizda\n\n"
            "Biz PUBG Mobile UC sotuvchi rasmiy botmiz.\n"
            "Savollar bo'yicha: {contact}"
        ),
        "order_approved_notify": (
            "✅ Buyurtmangiz #{order_id} tasdiqlandi!\n"
            "{amount} UC PUBG ID {pubg_id} manziliga yuborildi.\n"
            "Xaridingiz uchun rahmat! 🎉"
        ),
        "order_rejected_notify": (
            "❌ Buyurtmangiz #{order_id} rad etildi.\n"
            "Sabab: {reason}\n"
            "Savollar bo'yicha admin bilan bog'laning."
        ),
        "not_admin": "⛔ Sizda ruxsat yo'q.",
        "admin_panel": "🛠 Admin panel",
        "admin_pending_orders": "📥 Kutilayotgan buyurtmalar",
        "admin_manage_prices": "💰 Narxlarni boshqarish",
        "admin_manage_admins": "👤 Adminlarni boshqarish",
        "admin_stats": "📈 Statistika",
        "admin_no_pending": "Kutilayotgan buyurtmalar yo'q ✅",
        "admin_order_card": (
            "🧾 Buyurtma #{id}\n"
            "👤 Foydalanuvchi: {full_name} (@{username})\n"
            "🆔 Telegram ID: {telegram_id}\n"
            "🎮 PUBG ID: {pubg_id}\n"
            "💎 UC: {amount}\n"
            "💵 Narx: {price} so'm\n"
            "🕒 {created_at}"
        ),
        "approve": "✅ Tasdiqlash",
        "reject": "❌ Rad etish",
        "enter_reject_reason": "Rad etish sababini kiriting:",
        "order_approved_admin": "✅ Buyurtma #{id} tasdiqlandi va foydalanuvchiga xabar yuborildi.",
        "order_rejected_admin": "❌ Buyurtma #{id} rad etildi va foydalanuvchiga xabar yuborildi.",
        "choose_price_to_edit": "Tahrirlash uchun UC miqdorini tanlang:",
        "enter_new_price": "{amount} UC uchun yangi narxni kiriting (so'mda):",
        "price_updated": "✅ Narx yangilandi: {amount} UC — {price} so'm",
        "invalid_number": "❌ Faqat raqam kiriting.",
        "add_new_uc": "➕ Yangi UC miqdori qo'shish",
        "enter_new_uc_amount": "Yangi UC miqdorini kiriting:",
        "enter_new_uc_price": "{amount} UC uchun narxni kiriting (so'mda):",
        "add_admin_prompt": "➕ Admin qo'shish",
        "admin_added": "✅ Foydalanuvchi admin etib tayinlandi.",
        "user_not_found": "❌ Foydalanuvchi topilmadi. U avval botga /start bosishi kerak.",
        "remove_admin_prompt": "➖ Admin huquqini olib tashlash",
        "admin_removed": "✅ Admin huquqi olib tashlandi.",
        "back": "⬅️ Orqaga",
        "stats_text": (
            "📈 Umumiy statistika:\n\n"
            "👥 Foydalanuvchilar: {users}\n"
            "🧾 Jami buyurtmalar: {orders}\n"
            "⏳ Kutilayotgan: {pending}\n"
            "✅ Tasdiqlangan: {approved}\n"
            "❌ Rad etilgan: {rejected}\n"
        ),
    },
    "ru": {
        "welcome": "Привет, {name}! Используйте кнопки для работы с ботом 👇",
        "choose_language": "Tilni tanlang / Выберите язык:",
        "language_set": "✅ Язык переключен на русский",
        "menu_prices": "💹 Цены на UC",
        "menu_buy": "♻️ Купить UC",
        "menu_orders": "🧮 Список заказов",
        "menu_about": "👥 О нас",
        "menu_language": "🌐 Til / Язык",
        "prices_title": "📊 Актуальные цены на UC:\n\n",
        "price_line": "🔹 {amount} UC — {price} сум\n",
        "choose_uc_amount": "Выберите нужное количество UC:",
        "cancel_hint": "\nДля отмены: /cancel",
        "enter_pubg_id": "Введите PUBG Mobile Global ID:",
        "invalid_pubg_id": "❌ Неверный ID. Должен состоять только из цифр (5-15 знаков). Введите снова:",
        "confirm_order": (
            "🧾 Данные заказа:\n\n"
            "Количество UC: {amount} UC\n"
            "Цена: {price} сум\n"
            "PUBG ID: {pubg_id}\n\n"
            "Оплатите и отправьте чек (скриншот)."
        ),
        "send_receipt": "📎 Отправьте скриншот чека об оплате.",
        "not_a_photo": "❌ Чек должен быть отправлен изображением. Отправьте снова:",
        "order_created": (
            "✅ Ваш заказ принят!\n\n"
            "Номер заказа: #{order_id}\n"
            "Статус: ⏳ На рассмотрении\n\n"
            "Вы получите уведомление после подтверждения администратором."
        ),
        "cancelled": "❌ Действие отменено.",
        "nothing_to_cancel": "Нечего отменять.",
        "orders_empty": "У вас пока нет заказов.",
        "orders_stats": (
            "📊 Ваша статистика:\n\n"
            "✅ Подтверждено: {approved}\n"
            "⏳ Ожидает: {pending}\n"
            "❌ Отменено/отклонено: {rejected_cancelled}"
        ),
        "order_status_pending": "⏳ На рассмотрении",
        "order_status_approved": "✅ Подтвержден",
        "order_status_rejected": "❌ Отклонен",
        "order_status_cancelled": "❌ Отменен",
        "order_item": "#{id} | {amount} UC | {price} сум | {status}",
        "about_us": (
            "👥 О нас\n\n"
            "Мы официальный бот по продаже PUBG Mobile UC.\n"
            "По вопросам: {contact}"
        ),
        "order_approved_notify": (
            "✅ Ваш заказ #{order_id} подтвержден!\n"
            "{amount} UC отправлены на PUBG ID {pubg_id}.\n"
            "Спасибо за покупку! 🎉"
        ),
        "order_rejected_notify": (
            "❌ Ваш заказ #{order_id} отклонен.\n"
            "Причина: {reason}\n"
            "По вопросам обратитесь к администратору."
        ),
        "not_admin": "⛔ У вас нет доступа.",
        "admin_panel": "🛠 Админ-панель",
        "admin_pending_orders": "📥 Ожидающие заказы",
        "admin_manage_prices": "💰 Управление ценами",
        "admin_manage_admins": "👤 Управление админами",
        "admin_stats": "📈 Статистика",
        "admin_no_pending": "Нет ожидающих заказов ✅",
        "admin_order_card": (
            "🧾 Заказ #{id}\n"
            "👤 Пользователь: {full_name} (@{username})\n"
            "🆔 Telegram ID: {telegram_id}\n"
            "🎮 PUBG ID: <code>{pubg_id}</code> \n"
            "💎 UC: <b>{amount}</b> \n"
            "💵 Цена: {price} сум\n"
            "🕒 {created_at}"
        ),
        "approve": "✅ Подтвердить",
        "reject": "❌ Отклонить",
        "enter_reject_reason": "Введите причину отклонения:",
        "order_approved_admin": "✅ Заказ #{id} подтвержден, пользователь уведомлен.",
        "order_rejected_admin": "❌ Заказ #{id} отклонен, пользователь уведомлен.",
        "choose_price_to_edit": "Выберите количество UC для редактирования:",
        "enter_new_price": "Введите новую цену для {amount} UC (в сумах):",
        "price_updated": "✅ Цена обновлена: {amount} UC — {price} сум",
        "invalid_number": "❌ Введите только число.",
        "add_new_uc": "➕ Добавить новое количество UC",
        "enter_new_uc_amount": "Введите новое количество UC:",
        "enter_new_uc_price": "Введите цену для {amount} UC (в сумах):",
        "add_admin_prompt": "➕ Добавить админа",
        "admin_added": "✅ Пользователь назначен админом.",
        "user_not_found": "❌ Пользователь не найден. Он должен сначала нажать /start в боте.",
        "remove_admin_prompt": "➖ Снять права админа",
        "admin_removed": "✅ Права админа сняты.",
        "back": "⬅️ Назад",
        "stats_text": (
            "📈 Общая статистика:\n\n"
            "👥 Пользователей: {users}\n"
            "🧾 Всего заказов: {orders}\n"
            "⏳ Ожидают: {pending}\n"
            "✅ Подтверждено: {approved}\n"
            "❌ Отклонено: {rejected}\n"
        ),
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    lang = lang if lang in TRANSLATIONS else "uz"
    text = TRANSLATIONS[lang].get(key) or TRANSLATIONS["uz"].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
