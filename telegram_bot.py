# """
# OAK Jurnallari Telegram Bot
# Django API bilan integratsiya qilingan
#
# O'rnatish:
# pip install python-telegram-bot requests
#
# Ishga tushirish:
# python telegram_bot.py
# """
#
# import requests
# import logging
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     CallbackQueryHandler,
#     MessageHandler,
#     filters,
#     ContextTypes,
#     ConversationHandler
# )
#
# # Logging sozlash
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler('bot.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)
#
# # API base URL - o'z serveringiz manzilini kiriting
# API_BASE_URL = "http://127.0.0.1:8000/api"  # Local test uchun
# # API_BASE_URL = "https://oakjurnallari.uz/api"  # Production uchun
#
# # Conversation states
# CHOOSING_FAN, CHOOSING_BOLIM, SEARCHING_JURNAL = range(3)
#
#
# class JurnalBot:
#     """OAK Jurnallari Bot - Asosiy class"""
#
#     def __init__(self, token):
#         """Bot initializatsiya"""
#         self.token = token
#         self.app = Application.builder().token(token).build()
#         self.setup_handlers()
#         logger.info("Bot muvaffaqiyatli yaratildi")
#
#     def setup_handlers(self):
#         """Bot handlerlarini sozlash"""
#         # Conversation handler
#         conv_handler = ConversationHandler(
#             entry_points=[CommandHandler('start', self.start)],
#             states={
#                 CHOOSING_FAN: [CallbackQueryHandler(self.fan_chosen)],
#                 CHOOSING_BOLIM: [CallbackQueryHandler(self.bolim_chosen)],
#                 SEARCHING_JURNAL: [
#                     MessageHandler(filters.TEXT & ~filters.COMMAND, self.search_jurnal),
#                     CallbackQueryHandler(self.handle_jurnal_actions)
#                 ],
#             },
#             fallbacks=[
#                 CommandHandler('start', self.start),
#                 CommandHandler('cancel', self.cancel)
#             ],
#         )
#
#         # Handlerlarni qo'shish
#         self.app.add_handler(conv_handler)
#         self.app.add_handler(CommandHandler('help', self.help_command))
#         self.app.add_handler(CommandHandler('about', self.about_command))
#
#         logger.info("Handlerlar muvaffaqiyatli sozlandi")
#
#     async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Bot boshlanganda fanlarni ko'rsatish"""
#         logger.info(f"User {update.effective_user.id} botni boshladi")
#
#         try:
#             # Fanlarni olish
#             response = requests.get(f"{API_BASE_URL}/fanlar/", timeout=10)
#             response.raise_for_status()
#             fanlar = response.json()
#
#             if not fanlar:
#                 message_text = "❌ Fanlar topilmadi. Iltimos, keyinroq urinib ko'ring."
#                 if update.message:
#                     await update.message.reply_text(message_text)
#                 else:
#                     await update.callback_query.edit_message_text(message_text)
#                 return ConversationHandler.END
#
#             # Keyboard yaratish
#             keyboard = []
#             for fan in fanlar:
#                 keyboard.append([
#                     InlineKeyboardButton(
#                         f"📚 {fan['nomi']} ({fan['jurnallar_soni']})",
#                         callback_data=f"fan_{fan['id']}"
#                     )
#                 ])
#
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             message_text = (
#                 "🔬 *OAK Jurnallari Bot*\n\n"
#                 "Assalomu aleykum! Ilmiy jurnallarni qidirish botiga xush kelibsiz.\n\n"
#                 "📖 Bu bot orqali siz:\n"
#                 "• O'zbekiston Olimlar Akademiyasi jurnallarini topishingiz\n"
#                 "• Fan va bo'lim bo'yicha filtrlashingiz\n"
#                 "• Jurnal nomi orqali qidirishingiz mumkin\n\n"
#                 "👇 Quyidagi fanlardan birini tanlang:"
#             )
#
#             if update.message:
#                 await update.message.reply_text(
#                     message_text,
#                     reply_markup=reply_markup,
#                     parse_mode='Markdown'
#                 )
#             else:
#                 await update.callback_query.edit_message_text(
#                     message_text,
#                     reply_markup=reply_markup,
#                     parse_mode='Markdown'
#                 )
#
#             return CHOOSING_FAN
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"API xatolik: {e}")
#             error_text = (
#                 "❌ Server bilan bog'lanishda xatolik yuz berdi.\n"
#                 "Iltimos, keyinroq qayta urinib ko'ring.\n\n"
#                 "/start - Qaytadan boshlash"
#             )
#             if update.message:
#                 await update.message.reply_text(error_text)
#             else:
#                 await update.callback_query.edit_message_text(error_text)
#             return ConversationHandler.END
#         except Exception as e:
#             logger.error(f"Kutilmagan xatolik: {e}")
#             error_text = f"❌ Xatolik yuz berdi: {str(e)}\n\n/start - Qaytadan boshlash"
#             if update.message:
#                 await update.message.reply_text(error_text)
#             else:
#                 await update.callback_query.edit_message_text(error_text)
#             return ConversationHandler.END
#
#     async def fan_chosen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Fan tanlanganda bo'limlarni ko'rsatish"""
#         query = update.callback_query
#         await query.answer()
#
#         # Orqaga qaytish
#         if query.data == "back_to_fanlar":
#             return await self.start(update, context)
#
#         fan_id = query.data.split('_')[1]
#         context.user_data['fan_id'] = fan_id
#
#         logger.info(f"User {update.effective_user.id} fan tanladi: {fan_id}")
#
#         try:
#             # Tanlangan fanni olish
#             response = requests.get(f"{API_BASE_URL}/fanlar/{fan_id}/", timeout=10)
#             response.raise_for_status()
#             fan = response.json()
#             context.user_data['fan_nomi'] = fan['nomi']
#
#             # Bo'limlarni olish
#             response = requests.get(f"{API_BASE_URL}/bolimlar/", timeout=10)
#             response.raise_for_status()
#             bolimlar = response.json()
#
#             # Keyboard yaratish
#             keyboard = []
#             for bolim in bolimlar:
#                 keyboard.append([
#                     InlineKeyboardButton(
#                         f"🌍 {bolim['nomi']}",
#                         callback_data=f"bolim_{bolim['id']}"
#                     )
#                 ])
#
#             keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_fanlar")])
#
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             await query.edit_message_text(
#                 f"📚 *{fan['nomi']}*\n\n"
#                 f"Jurnallar soni: {fan['jurnallar_soni']} ta\n\n"
#                 f"👇 Bo'limni tanlang:",
#                 reply_markup=reply_markup,
#                 parse_mode='Markdown'
#             )
#
#             return CHOOSING_BOLIM
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"API xatolik: {e}")
#             await query.edit_message_text(
#                 f"❌ Server bilan bog'lanishda xatolik.\n\n/start - Qaytadan boshlash"
#             )
#             return ConversationHandler.END
#         except Exception as e:
#             logger.error(f"Xatolik: {e}")
#             await query.edit_message_text(f"❌ Xatolik: {str(e)}\n\n/start - Qaytadan boshlash")
#             return ConversationHandler.END
#
#     async def bolim_chosen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Bo'lim tanlanganda jurnallarni ko'rsatish"""
#         query = update.callback_query
#         await query.answer()
#
#         # Orqaga qaytish
#         if query.data.startswith("back_to_"):
#             fan_id = context.user_data.get('fan_id')
#             if query.data == "back_to_fanlar":
#                 return await self.start(update, context)
#             elif fan_id:
#                 # Fan tanlash sahifasiga qaytish
#                 query.data = f"fan_{fan_id}"
#                 return await self.fan_chosen(update, context)
#
#         bolim_id = query.data.split('_')[1]
#         fan_id = context.user_data.get('fan_id')
#
#         context.user_data['bolim_id'] = bolim_id
#
#         logger.info(f"User {update.effective_user.id} bo'lim tanladi: {bolim_id}")
#
#         try:
#             # Jurnallarni olish
#             response = requests.get(
#                 f"{API_BASE_URL}/jurnallar/",
#                 params={'fan': fan_id, 'bolim': bolim_id, 'page_size': 20},
#                 timeout=10
#             )
#             response.raise_for_status()
#             data = response.json()
#             jurnallar = data.get('results', [])
#             total_count = data.get('count', 0)
#
#             if not jurnallar:
#                 keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"fan_{fan_id}")]]
#                 reply_markup = InlineKeyboardMarkup(keyboard)
#                 await query.edit_message_text(
#                     "❌ Bu bo'limda jurnallar topilmadi.\n\n"
#                     "Boshqa bo'limni tanlang.",
#                     reply_markup=reply_markup
#                 )
#                 return CHOOSING_BOLIM
#
#             # Jurnallar ro'yxatini ko'rsatish
#             keyboard = []
#             for jurnal in jurnallar[:20]:  # Faqat 20 tasini ko'rsatish
#                 # Jurnal nomini qisqartirish (40 belgidan uzun bo'lsa)
#                 jurnal_nomi = jurnal['nomi']
#                 if len(jurnal_nomi) > 40:
#                     jurnal_nomi = jurnal_nomi[:37] + "..."
#
#                 keyboard.append([
#                     InlineKeyboardButton(
#                         f"📄 {jurnal_nomi}",
#                         callback_data=f"jurnal_{jurnal['id']}"
#                     )
#                 ])
#
#             # Qo'shimcha tugmalar
#             keyboard.append([InlineKeyboardButton("🔍 Qidiruv", callback_data="search")])
#             keyboard.append([
#                 InlineKeyboardButton("⬅️ Orqaga", callback_data=f"fan_{fan_id}"),
#                 InlineKeyboardButton("🏠 Bosh sahifa", callback_data="back_to_fanlar")
#             ])
#
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             await query.edit_message_text(
#                 f"📖 *Jurnallar ro'yxati*\n\n"
#                 f"📊 Jami: {total_count} ta jurnal\n"
#                 f"📄 Ko'rsatilmoqda: {len(jurnallar)} ta\n\n"
#                 f"👇 Jurnalni tanlang yoki qidiring:",
#                 reply_markup=reply_markup,
#                 parse_mode='Markdown'
#             )
#
#             return SEARCHING_JURNAL
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"API xatolik: {e}")
#             await query.edit_message_text(
#                 f"❌ Jurnallarni yuklashda xatolik.\n\n/start - Qaytadan boshlash"
#             )
#             return ConversationHandler.END
#         except Exception as e:
#             logger.error(f"Xatolik: {e}")
#             await query.edit_message_text(f"❌ Xatolik: {str(e)}\n\n/start - Qaytadan boshlash")
#             return ConversationHandler.END
#
#     async def search_jurnal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Jurnal qidirish"""
#         search_query = update.message.text.strip()
#         fan_id = context.user_data.get('fan_id')
#         bolim_id = context.user_data.get('bolim_id')
#
#         logger.info(f"User {update.effective_user.id} qidiruv: {search_query}")
#
#         # Juda qisqa qidiruv so'rovlarini rad etish
#         if len(search_query) < 2:
#             await update.message.reply_text(
#                 "❌ Qidiruv so'rovi juda qisqa.\n"
#                 "Kamida 2 ta belgi kiriting."
#             )
#             return SEARCHING_JURNAL
#
#         try:
#             # Qidiruv
#             response = requests.get(
#                 f"{API_BASE_URL}/jurnallar/",
#                 params={
#                     'fan': fan_id,
#                     'bolim': bolim_id,
#                     'q': search_query,
#                     'page_size': 10
#                 },
#                 timeout=10
#             )
#             response.raise_for_status()
#             data = response.json()
#             jurnallar = data.get('results', [])
#             total_count = data.get('count', 0)
#
#             if not jurnallar:
#                 await update.message.reply_text(
#                     f"❌ *\"{search_query}\"* bo'yicha hech narsa topilmadi.\n\n"
#                     "💡 Maslahat:\n"
#                     "• Boshqa nom bilan qidiring\n"
#                     "• Qisqaroq so'z kiriting\n"
#                     "• Inglizcha nom bilan urinib ko'ring\n\n"
#                     "Yoki /start bosing.",
#                     parse_mode='Markdown'
#                 )
#                 return SEARCHING_JURNAL
#
#             # Natijalarni ko'rsatish
#             keyboard = []
#             for jurnal in jurnallar[:10]:
#                 # Jurnal nomini qisqartirish
#                 jurnal_nomi = jurnal['nomi']
#                 if len(jurnal_nomi) > 40:
#                     jurnal_nomi = jurnal_nomi[:37] + "..."
#
#                 keyboard.append([
#                     InlineKeyboardButton(
#                         f"📄 {jurnal_nomi}",
#                         callback_data=f"jurnal_{jurnal['id']}"
#                     )
#                 ])
#
#             keyboard.append([
#                 InlineKeyboardButton("⬅️ Orqaga", callback_data=f"bolim_{bolim_id}"),
#                 InlineKeyboardButton("🏠 Bosh sahifa", callback_data="back_to_fanlar")
#             ])
#
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             await update.message.reply_text(
#                 f"🔍 *Qidiruv natijalari:* \"{search_query}\"\n\n"
#                 f"📊 Topildi: {total_count} ta jurnal\n"
#                 f"📄 Ko'rsatilmoqda: {len(jurnallar)} ta\n\n"
#                 f"👇 Jurnalni tanlang:",
#                 reply_markup=reply_markup,
#                 parse_mode='Markdown'
#             )
#
#             return SEARCHING_JURNAL
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"API xatolik: {e}")
#             await update.message.reply_text(
#                 "❌ Qidiruvda xatolik yuz berdi.\n\n/start - Qaytadan boshlash"
#             )
#             return SEARCHING_JURNAL
#         except Exception as e:
#             logger.error(f"Xatolik: {e}")
#             await update.message.reply_text(f"❌ Xatolik: {str(e)}")
#             return SEARCHING_JURNAL
#
#     async def handle_jurnal_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Jurnal bilan bog'liq barcha action'larni boshqarish"""
#         query = update.callback_query
#         await query.answer()
#
#         # Qidiruv boshlash
#         if query.data == "search":
#             await query.message.reply_text(
#                 "🔍 *Qidiruv*\n\n"
#                 "Jurnal nomini kiriting:\n"
#                 "(Masalan: Journal of Chemistry)",
#                 parse_mode='Markdown'
#             )
#             return SEARCHING_JURNAL
#
#         # Orqaga qaytish
#         if query.data.startswith("bolim_"):
#             return await self.bolim_chosen(update, context)
#
#         if query.data == "back_to_fanlar":
#             return await self.start(update, context)
#
#         # Jurnal tafsilotlarini ko'rsatish
#         if query.data.startswith("jurnal_"):
#             return await self.show_jurnal_detail(update, context)
#
#         return SEARCHING_JURNAL
#
#     async def show_jurnal_detail(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Jurnal tafsilotlarini ko'rsatish"""
#         query = update.callback_query
#         jurnal_id = query.data.split('_')[1]
#
#         logger.info(f"User {update.effective_user.id} jurnal ko'rmoqda: {jurnal_id}")
#
#         try:
#             # Jurnal tafsilotlarini olish
#             response = requests.get(f"{API_BASE_URL}/jurnallar/{jurnal_id}/", timeout=10)
#             response.raise_for_status()
#             jurnal = response.json()
#
#             # Ma'lumotlarni formatlash
#             text = f"📖 *{jurnal['nomi']}*\n\n"
#             text += f"🔬 *Fan:* {jurnal['fan_nomi']}\n"
#             text += f"🌍 *Bo'lim:* {jurnal['bolim_nomi']}\n\n"
#
#             if jurnal.get('nashr_chastotasi'):
#                 text += f"📅 *Nashr chastotasi:* {jurnal['nashr_chastotasi']}\n"
#
#             if jurnal.get('jurnal_sayti'):
#                 text += f"🌐 *Jurnal sayti:*\n{jurnal['jurnal_sayti']}\n"
#
#             if jurnal.get('murojaat_link'):
#                 text += f"\n✉️ *Murojaat uchun:*\n{jurnal['murojaat_link']}\n"
#
#             if jurnal.get('talablar_link'):
#                 text += f"\n📋 *Talablar:*\n{jurnal['talablar_link']}\n"
#
#             bolim_id = context.user_data.get('bolim_id')
#             keyboard = [
#                 [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"bolim_{bolim_id}")],
#                 [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="back_to_fanlar")]
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             # Agar rasm bo'lsa, uni yuborish
#             if jurnal.get('rasmi_url'):
#                 try:
#                     await query.message.reply_photo(
#                         photo=jurnal['rasmi_url'],
#                         caption=text,
#                         reply_markup=reply_markup,
#                         parse_mode='Markdown'
#                     )
#                     # Eski xabarni o'chirish
#                     try:
#                         await query.message.delete()
#                     except:
#                         pass
#                 except Exception as photo_error:
#                     logger.error(f"Rasm yuklashda xatolik: {photo_error}")
#                     # Agar rasm yuklanmasa, matn ko'rinishida yuborish
#                     await query.edit_message_text(
#                         text=text,
#                         reply_markup=reply_markup,
#                         parse_mode='Markdown',
#                         disable_web_page_preview=True
#                     )
#             else:
#                 await query.edit_message_text(
#                     text=text,
#                     reply_markup=reply_markup,
#                     parse_mode='Markdown',
#                     disable_web_page_preview=True
#                 )
#
#             return SEARCHING_JURNAL
#
#         except requests.exceptions.RequestException as e:
#             logger.error(f"API xatolik: {e}")
#             await query.message.reply_text(
#                 "❌ Jurnal ma'lumotlarini yuklashda xatolik.\n\n/start - Qaytadan boshlash"
#             )
#             return SEARCHING_JURNAL
#         except Exception as e:
#             logger.error(f"Xatolik: {e}")
#             await query.message.reply_text(f"❌ Xatolik: {str(e)}")
#             return SEARCHING_JURNAL
#
#     async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Bekor qilish"""
#         await update.message.reply_text(
#             "❌ Bekor qilindi.\n\n"
#             "/start - Qaytadan boshlash"
#         )
#         return ConversationHandler.END
#
#     async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Yordam ko'rsatish"""
#         help_text = (
#             "📚 *OAK Jurnallari Bot - Yordam*\n\n"
#             "*Buyruqlar:*\n"
#             "/start - Botni boshlash\n"
#             "/help - Yordam\n"
#             "/about - Bot haqida\n"
#             "/cancel - Bekor qilish\n\n"
#             "*Qanday foydalanish:*\n"
#             "1️⃣ Fanni tanlang\n"
#             "2️⃣ Bo'limni tanlang\n"
#             "3️⃣ Jurnalni tanlang yoki qidiring\n\n"
#             "*Xususiyatlar:*\n"
#             "• 📖 Barcha OAK jurnallari\n"
#             "• 🔍 Jurnal bo'yicha qidiruv\n"
#             "• 🌐 To'liq ma'lumot va havolalar\n"
#             "• 🖼 Jurnal rasmlari\n\n"
#             "*Texnik yordam:*\n"
#             "Muammo bo'lsa: @your_support\n"
#             "Sayt: oakjurnallari.uz"
#         )
#
#         await update.message.reply_text(help_text, parse_mode='Markdown')
#
#     async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         """Bot haqida ma'lumot"""
#         about_text = (
#             "ℹ️ *Bot haqida*\n\n"
#             "📚 *OAK Jurnallari Bot*\n"
#             "Versiya: 1.0.0\n\n"
#             "Bu bot O'zbekiston Olimlar Akademiyasi tomonidan "
#             "tasdiqlangan ilmiy jurnallar haqida ma'lumot beradi.\n\n"
#             "*Imkoniyatlar:*\n"
#             "• Fan bo'yicha filtrlash\n"
#             "• Bo'lim bo'yicha filtrlash\n"
#             "• Jurnal nomi orqali qidiruv\n"
#             "• To'liq jurnal ma'lumotlari\n\n"
#             "*Texnologiyalar:*\n"
#             "• Python Telegram Bot\n"
#             "• Django REST API\n"
#             "• PostgreSQL/SQLite\n\n"
#             "🌐 *Sayt:* oakjurnallari.uz\n"
#             "📧 *Aloqa:* @your_support\n\n"
#             "© 2025 OAK Jurnallari"
#         )
#
#         await update.message.reply_text(about_text, parse_mode='Markdown')
#
#     def run(self):
#         """Botni ishga tushirish"""
#         logger.info("Bot ishga tushirilmoqda...")
#         print("🤖 Bot ishga tushdi!")
#         print(f"📡 API: {API_BASE_URL}")
#         print("⏳ Xabarlar kutilmoqda...")
#         print("🛑 To'xtatish uchun: Ctrl+C\n")
#
#         self.app.run_polling(
#             allowed_updates=Update.ALL_TYPES,
#             drop_pending_updates=True
#         )
#
#
# # Botni ishga tushirish
# if __name__ == '__main__':
#     # ⚠️ DIQQAT: Bu yerga o'z bot tokeningizni kiriting!
#     BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
#
#     # Token tekshirish
#     if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
#         print("❌ XATO: Bot tokenini kiritmadingiz!")
#         print("\n📝 Qanday qilib token olish:")
#         print("1. Telegram'da @BotFather ni toping")
#         print("2. /newbot buyrug'ini yuboring")
#         print("3. Bot nomini kiriting")
#         print("4. Bot username kiriting (@... bilan tugashi kerak)")
#         print("5. Tokenni oling va BOT_TOKEN o'zgaruvchisiga kiriting\n")
#         exit(1)
#
#     try:
#         # Botni yaratish va ishga tushirish
#         bot = JurnalBot(BOT_TOKEN)
#         bot.run()
#     except KeyboardInterrupt:
#         logger.info("Bot to'xtatildi (Ctrl+C)")
#         print("\n👋 Bot to'xtatildi!")
#     except Exception as e:
#         logger.error(f"Bot ishga tushirishda xatolik: {e}")
#         print(f"\n❌ Xatolik: {e}")