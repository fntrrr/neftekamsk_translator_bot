import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("Не найден API_TOKEN!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

TRANSLATION_MAP = {
    'а': 'a', 'б': '6', 'в': 'B', 'г': 'r', 'д': 'D',
    'е': 'E', 'ё': 'e', 'ж': '}|{', 'з': '3', 'и': 'u',
    'й': 'u', 'к': 'K', 'л': 'J|', 'м': 'M', 'н': 'H',
    'о': 'O', 'п': 'TT', 'р': 'P', 'с': 'C', 'т': 'T',
    'у': 'y', 'ф': '%', 'х': 'X', 'ц': 'LI,', 'ч': '4',
    'ш': 'LLI', 'щ': 'LLI,', 'ъ': "'b", 'ы': 'bI', 'ь': 'b',
    'э': 'E', 'ю': '}O', 'я': '9',
    ' ': ' ',
}


def translate_text(text: str) -> str:
    result = []
    for char in text.lower():
        result.append(TRANSLATION_MAP.get(char, char))
    return "".join(result)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "TTPuBET! 9 6OT-TTEPEBOD4uK.\n\n"
        "1️⃣ OTTTPaBb MHE TEKCT B J|u4HbIE COO6LLI,EHu9.\n"
        "2️⃣ uJ|u uCTTOJ|b3yu uHJ|auH: HaTTuLLIu @username_bot TBOu_TEKCT B J|}O6OM 4aTE."
    )


@dp.message()
async def echo_handler(message: types.Message):
    if message.text:
        translated_text = translate_text(message.text)
        await message.answer(translated_text)


@dp.inline_query()
async def inline_query_handler(query: types.InlineQuery):
    try:
        text = query.query
        logging.info(f"Получен inline запрос: '{text}'")

        if not text:
            results = [
                types.InlineQueryResultArticle(
                    id="hint",
                    title="TTEPEBEDeHHbIu TEKCT",
                    description="TTPuMEP: @neftekinsktranslator_bot привет",
                    input_message_content=types.InputTextMessageContent(
                        message_text="KTO HaTTuCaJ| ETOT 4EPTOB TEKCT 6J|9Tb"
                    ),
                )
            ]
        else:
            translated = translate_text(text)
            logging.info(f"TTEPEBEDeHHbIu TEKCT: '{translated}'")

            results = [
                types.InlineQueryResultArticle(
                    id="main",
                    title=f" TTEPEBECTu TEKCT",
                    description=translated[:40] + ("..." if len(translated) > 40 else ""),
                    input_message_content=types.InputTextMessageContent(
                        message_text=translated
                    ),
                    thumbnail_url="https://i.postimg.cc/7YXQbSPz/put.png",
                )
            ]

        await query.answer(results, cache_time=0)
        logging.info("Inline ответ отправлен")

    except Exception as e:
        logging.error(f"Ошибка в inline handler: {e}")
        import traceback
        traceback.print_exc()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())
