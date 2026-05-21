# =========================
# ZERO MAKS BOT
# pyTelegramBotAPI
# =========================

# INSTALL:
# pip install pyTelegramBotAPI

import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# =========================
# SETTINGS
# =========================

BOT_TOKEN = "8767223581:AAHcaekUAnascE8YnM1jaTlJzRPxbC_gNMM"

GROUP_ID = -1003511488835

bot = telebot.TeleBot(BOT_TOKEN)

orders = {}

# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    order_btn = KeyboardButton("🛒 Buyurtma berish")

    kb.add(order_btn)

    bot.send_message(
        message.chat.id,
        """
🍔 Zero Maks botiga xush kelibsiz

⬇️ Pastdagi chap tugmani bosing
va buyurtma bering.
""",
        reply_markup=kb
    )

# =========================
# ORDER BUTTON
# =========================

@bot.message_handler(func=lambda m: m.text == "🛒 Buyurtma berish")
def order(message):

    user_id = message.from_user.id
    username = message.from_user.first_name

    # MISOL PRODUCTLAR
    products = [
        "Lavash",
        "Burger",
        "Cola"
    ]

    order_id = len(orders) + 1

    orders[order_id] = {
        "user_id": user_id,
        "products": products
    }

    text = f"""
🛒 Yangi zakaz #{order_id}

👤 Mijoz: {username}

📦 Lavash
📦 Burger
📦 Cola
"""

    kb = InlineKeyboardMarkup()

    # PRODUCT BUTTONS
    for p in products:
        kb.add(
            InlineKeyboardButton(
                text=f"❌ {p} qolmagan",
                callback_data=f"no|{order_id}|{p}"
            )
        )

    # CONFIRM
    kb.add(
        InlineKeyboardButton(
            text="✅ Tasdiqlash",
            callback_data=f"ok|{order_id}"
        )
    )

    # SEND TO GROUP
    bot.send_message(
        GROUP_ID,
        text,
        reply_markup=kb
    )

    bot.send_message(
        message.chat.id,
        "✅ Buyurtmangiz yuborildi"
    )

# =========================
# PRODUCT NOT AVAILABLE
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("no|")
)
def no_product(call):

    data = call.data.split("|")

    order_id = int(data[1])
    product_name = data[2]

    order = orders.get(order_id)

    if not order:
        return

    user_id = order["user_id"]

    # USER MESSAGE
    bot.send_message(
        user_id,
        f"""
❌ Sizning zakazingiz qabul qilinmadi

Sabab:
📦 {product_name} qolmagan.
"""
    )

    bot.answer_callback_query(
        call.id,
        f"{product_name} yuborildi"
    )

# =========================
# CONFIRM ORDER
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("ok|")
)
def confirm(call):

    data = call.data.split("|")

    order_id = int(data[1])

    order = orders.get(order_id)

    if not order:
        return

    user_id = order["user_id"]

    bot.send_message(
        user_id,
        """
✅ Zakazingiz qabul qilindi

🚚 Operator tez orada siz bilan bog‘lanadi.
"""
    )

    bot.answer_callback_query(
        call.id,
        "Zakaz tasdiqlandi"
    )

# =========================
# RUN
# =========================

print("BOT ISHLADI")

bot.infinity_polling()