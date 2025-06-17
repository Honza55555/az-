from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Texty pro jednotlivé části v češtině a angličtině
TEXTS = {
    "start": {
        "cs": "☕️ Vítejte v Coffee Perk!\nTěší nás, že jste tu. 🌟\nProsím, vyberte si jazyk. 🗣️",
        "en": "☕️ Welcome to Coffee Perk!\nWe’re happy to see you here. 🌟\nPlease choose your language. 🗣️"
    },
    "menu_prompt": {
        "cs": "Na co se mě můžeš zeptat:",
        "en": "What can you ask me about:"
    },
    "menu_buttons": {
        "cs": [
            ("🧾 Menu a nabídka", "menu"),
            ("🕐 Otevírací doba", "hours"),
            ("📍 Kde nás najdete", "location"),
            ("📞 Kontakt / Rezervace", "contact"),
            ("📦 Předobjednávka (již brzy)", "preorder"),
            ("😎 Proč si zajít na kávu", "reasons")
        ],
        "en": [
            ("🧾 Menu & Offer", "menu"),
            ("🕐 Opening Hours", "hours"),
            ("📍 Location", "location"),
            ("📞 Contact / Reservation", "contact"),
            ("📦 Pre-order (coming soon)", "preorder"),
            ("😎 Why visit us?", "reasons")
        ]
    },
    "sections": {
        "menu": {
            "cs": (
                "🥐 COFFEE PERK MENU ☕️\n"
                "U nás nejde jen o kafe. Je to malý rituál. Je to nálada. Je to... láska v šálku. 💘\n\n"
                "☕ Výběrová káva\n🍳 Snídaně (lehké i pořádné)\n🍰 Domácí dorty\n🥗 Brunch a saláty\n\n"
                "📄 Kompletní menu:\n👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
                "Ať už si dáte espresso, matchu nebo zázvorovku – tady to chutná líp. 💛"
            ),
            "en": (
                "🥐 COFFEE PERK MENU ☕️\n"
                "It’s not just coffee here. It’s a small ritual. It’s a mood. It’s... love in a cup. 💘\n\n"
                "☕ Specialty coffee\n🍳 Breakfast (light & hearty)\n🍰 Homemade cakes\n🥗 Brunch & salads\n\n"
                "📄 Full menu:\n👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
                "Whether it’s an espresso, matcha, or ginger latte – it tastes better here. 💛"
            )
        },
        "hours": {
            "cs": (
                "🕐 KDY MÁME OTEVŘENO?\n\n"
                "📅 Pondělí–Pátek: 7:30 – 17:00\n"
                "📅 Sobota & Neděle: ZAVŘENO\n\n"
                "Chcete nás navštívit? Jsme tu každý všední den od brzkého rána.\n"
                "Těšíme se na vás! ☕"
            ),
            "en": (
                "🕐 OPENING HOURS\n\n"
                "📅 Monday–Friday: 7:30 AM – 5:00 PM\n"
                "📅 Saturday & Sunday: CLOSED\n\n"
                "Planning a visit? We’re here every weekday early morning.\n"
                "Looking forward to seeing you! ☕"
            )
        },
        "location": {
            "cs": (
                "📍 KDE NÁS NAJDETE?\n\n"
                "🏠 Vyskočilova 1100/2, Praha 4\n"
                "🗺️ Mapa: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
                "Najdete nás snadno – stylová kavárna, příjemná atmosféra a lidi, co kávu berou vážně i s úsměvem.\n"
                "Zastavte se. Na chvilku nebo na celý den."
            ),
            "en": (
                "📍 WHERE TO FIND US?\n\n"
                "🏠 Vyskočilova 1100/2, Prague 4\n"
                "🗺️ Map: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
                "Easy to find – a stylish café, a cozy atmosphere, and people who take coffee seriously with a smile.\n"
                "Drop by for a moment or a whole day."
            )
        },
        "contact": {
            "cs": (
                "📞 KONTAKTUJTE NÁS\n\n"
                "📬 E-mail: info@coffeeperk.cz\n"
                "📞 Telefon: +420 725 422 518\n\n"
                "Rádi vám pomůžeme s rezervací, odpovíme na vaše dotazy nebo poradíme s výběrem.\n"
                "Neváhejte se nám ozvat – jsme tu pro vás."
            ),
            "en": (
                "📞 CONTACT US\n\n"
                "📬 Email: info@coffeeperk.cz\n"
                "📞 Phone: +420 725 422 518\n\n"
                "We’re happy to assist with reservations, answer your questions, or recommend our favorites.\n"
                "Don’t hesitate to reach out – we’re here for you."
            )
        },
        "preorder": {
            "cs": (
                "📦 PŘEDOBJEDNÁVKY\n\n"
                "Brzy spustíme možnost objednat si kávu a snídani předem přes Telegram.\n"
                "Zatím nás navštivte osobně – těšíme se! ☕️"
            ),
            "en": (
                "📦 PRE-ORDERS\n\n"
                "Soon you’ll be able to pre-order your coffee and breakfast via Telegram.\n"
                "For now, visit us in person – we can’t wait to see you! ☕️"
            )
        },
        "reasons": {
            "cs": (
                "😎 DŮVODY, PROČ SI ZAJÍT NA KÁVU\n\n"
                "☕ Protože svět se lépe řeší s kofeinem.\n"
                "📚 Protože práce počká – espresso ne.\n"
                "💬 Protože dobrá konverzace začíná u šálku.\n"
                "👀 Protože dnes jste už skoro byli produktivní.\n"
                "🧠 Protože mozek startuje až po druhé kávě.\n"
                "🌦️ Protože venku prší... nebo svítí slunce... nebo prostě cítíte, že je čas.\n\n"
                "A někdy netřeba důvod. Prostě jen přijďte. 💛"
            ),
            "en": (
                "😎 REASONS TO VISIT US\n\n"
                "☕ Because the world is better with caffeine.\n"
                "📚 Because work can wait – espresso can’t.\n"
                "💬 Because great conversations start over a cup.\n"
                "👀 Because you’re almost productive today, right?\n"
                "🧠 Because the brain really kicks in after the second cup.\n"
                "🌦️ Because it’s raining... or sunny... or you just feel it’s time.\n\n"
                "And sometimes no reason is needed. Just come by. 💛"
            )
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇨🇿 Čeština", callback_data='lang_cs'),
         InlineKeyboardButton("🌍 English", callback_data='lang_en')]
    ]
    await update.message.reply_text(
        TEXTS['start']['cs'],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    # Jazyk vybrán
    if data.startswith('lang_'):
        lang = data.split('_')[1]
        context.user_data['lang'] = lang
        # Zobrazit hlavní menu
        text = TEXTS['menu_prompt'][lang]
        buttons = TEXTS['menu_buttons'][lang]
        keyboard = [[InlineKeyboardButton(label, callback_data=key)] for label, key in buttons]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    # Sekce vybrána
    lang = context.user_data.get('lang', 'cs')
    section = TEXTS['sections'][data][lang]
    await query.edit_message_text(section)

if __name__ == '__main__':
    token = os.getenv('BOT_TOKEN')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
