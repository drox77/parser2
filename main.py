import asyncio
import os
import logging
import time
import random
import sys
from typing import List, Dict
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
    FSInputFile
)
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 🔑 ТОКЕН БОТА
BOT_TOKEN = "8265374266:AAGLfYdq1sJg_PPBQAngW84E6u5BCgj3_BY"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# 🎁 NFT GIFTS КОЛЛЕКЦИИ (30 коллекций)
NFT_GIFT_COLLECTIONS = {
    "snoop-dogg": {
        "name": "🐕 Snoop Dogg",
        "base_url": "https://t.me/nft/SnoopDogg-",
        "max_number": 577000,
        "description": "Легендарный репер Snoop Dogg NFT"
    },
    "swag-bag": {
        "name": "🎒 Swag Bag",
        "base_url": "https://t.me/nft/SwagBag-",
        "max_number": 230000,
        "description": "Стильная сумка с NFT"
    },
    "snoop-cigar": {
        "name": "🚬 Snoop Cigar",
        "base_url": "https://t.me/nft/SnoopCigar-",
        "max_number": 116000,
        "description": "Сигара от Snoop Dogg"
    },
    "ice-cream": {
        "name": "🍦 Ice Cream",
        "base_url": "https://t.me/nft/IceCream-",
        "max_number": 319000,
        "description": "Вкусное мороженое NFT"
    },
    "easter-egg": {
        "name": "🥚 Easter Egg",
        "base_url": "https://t.me/nft/EasterEgg-",
        "max_number": 160000,
        "description": "Пасхальное яйцо с сюрпризом"
    },
    "spring-basket": {
        "name": "🌷 Spring Basket",
        "base_url": "https://t.me/nft/SpringBasket-",
        "max_number": 158000,
        "description": "Весенняя корзинка NFT"
    },
    "jack-in-the-box": {
        "name": "🎁 Jack In The Box",
        "base_url": "https://t.me/nft/JackInTheBox-",
        "max_number": 95000,
        "description": "Сюрприз в коробке"
    },
    "stellar-rocket": {
        "name": "🚀 Stellar Rocket",
        "base_url": "https://t.me/nft/StellarRocket-",
        "max_number": 132000,
        "description": "Космическая ракета NFT"
    },
    "jolly-chimp": {
        "name": "🐵 Jolly Chimp",
        "base_url": "https://t.me/nft/JollyChimp-",
        "max_number": 113000,
        "description": "Веселый шимпанзе NFT"
    },
    "happy-brownie": {
        "name": "🍫 Happy Brownie",
        "base_url": "https://t.me/nft/HappyBrownie-",
        "max_number": 203000,
        "description": "Шоколадный брауни NFT"
    },
    "instant-ramen": {
        "name": "🍜 Instant Ramen",
        "base_url": "https://t.me/nft/InstantRamen-",
        "max_number": 349000,
        "description": "Лапша быстрого приготовления"
    },
    "faith-amulet": {
        "name": "📿 Faith Amulet",
        "base_url": "https://t.me/nft/FaithAmulet-",
        "max_number": 128000,
        "description": "Амулет веры NFT"
    },
    "clover-pin": {
        "name": "🍀 Clover Pin",
        "base_url": "https://t.me/nft/CloverPin-",
        "max_number": 218000,
        "description": "Клевер на удачу"
    },
    "money-pot": {
        "name": "💰 Money Pot",
        "base_url": "https://t.me/nft/MoneyPot-",
        "max_number": 62000,
        "description": "Горшок с деньгами NFT"
    },
    "pretty-posy": {
        "name": "💐 Pretty Posy",
        "base_url": "https://t.me/nft/PrettyPosy-",
        "max_number": 95000,
        "description": "Красивый букет NFT"
    },
    "bow-tie": {
        "name": "🎀 Bow Tie",
        "base_url": "https://t.me/nft/BowTie-",
        "max_number": 53000,
        "description": "Элегантный галстук-бабочка"
    },
    "light-sword": {
        "name": "⚔️ Light Sword",
        "base_url": "https://t.me/nft/LightSword-",
        "max_number": 123000,
        "description": "Световой меч NFT"
    },
    "fresh-socks": {
        "name": "🧦 Fresh Socks",
        "base_url": "https://t.me/nft/FreshSocks-",
        "max_number": 152000,
        "description": "Свежие носки NFT"
    },
    "input-key": {
        "name": "🔑 Input Key",
        "base_url": "https://t.me/nft/InputKey-",
        "max_number": 122000,
        "description": "Ключ для ввода NFT"
    },
    "lunar-snake": {
        "name": "🌙🐍 Lunar Snake",
        "base_url": "https://t.me/nft/LunarSnake-",
        "max_number": 180000,
        "description": "Лунная змея NFT"
    },
    "big-year": {
        "name": "📅 Big Year",
        "base_url": "https://t.me/nft/BigYear-",
        "max_number": 71000,
        "description": "Большой годовой календарь"
    },
    "pet-snake": {
        "name": "🐍 Pet Snake",
        "base_url": "https://t.me/nft/PetSnake-",
        "max_number": 160000,
        "description": "Домашняя змея NFT"
    },
    "snake-box": {
        "name": "📦🐍 Snake Box",
        "base_url": "https://t.me/nft/SnakeBox-",
        "max_number": 156000,
        "description": "Коробка со змеей"
    },
    "winter-wreath": {
        "name": "🎄 Winter Wreath",
        "base_url": "https://t.me/nft/WinterWreath-",
        "max_number": 67000,
        "description": "Зимний венок NFT"
    },
    "ginger-cookie": {
        "name": "🍪 Ginger Cookie",
        "base_url": "https://t.me/nft/GingerCookie-",
        "max_number": 135000,
        "description": "Имбирное печенье NFT"
    },
    "snow-globe": {
        "name": "🔮 Snow Globe",
        "base_url": "https://t.me/nft/SnowGlobe-",
        "max_number": 49000,
        "description": "Снежный шар NFT"
    },
    "star-notepad": {
        "name": "📓 Star Notepad",
        "base_url": "https://t.me/nft/StarNotepad-",
        "max_number": 66000,
        "description": "Звездный блокнот NFT"
    },
    "jelly-bunny": {
        "name": "🐰 Jelly Bunny",
        "base_url": "https://t.me/nft/JellyBunny-",
        "max_number": 98000,
        "description": "Желейный кролик NFT"
    },
    "lol-pop": {
        "name": "🍭 Lol Pop",
        "base_url": "https://t.me/nft/LolPop-",
        "max_number": 427000,
        "description": "Сладкая конфета NFT"
    },
    "desk-calendar": {
        "name": "📅 Desk Calendar",
        "base_url": "https://t.me/nft/DeskCalendar-",
        "max_number": 339000,
        "description": "Настольный календарь NFT"
    },
}

# История генерации
generation_history = []

# Выбранные коллекции
selected_collections = set()

# 🎨 КНОПКИ
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🔗 ГЕНЕРИРОВАТЬ ССЫЛКИ", callback_data="generate_links")],
        [InlineKeyboardButton(text="🎯 ВЫБРАТЬ КОЛЛЕКЦИИ", callback_data="select_collections")],
        [InlineKeyboardButton(text="⚡ БЫСТРАЯ ГЕНЕРАЦИЯ", callback_data="quick_generate")],
        [InlineKeyboardButton(text="📊 ИСТОРИЯ", callback_data="show_history")],
        [InlineKeyboardButton(text="ℹ️ ИНФО", callback_data="info")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_collections_keyboard(show_selection=True):
    buttons = []
    for coll_id, coll_data in NFT_GIFT_COLLECTIONS.items():
        if show_selection and coll_id in selected_collections:
            text = f"✅ {coll_data['name']}"
        else:
            text = coll_data['name']
        
        buttons.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"collection_{coll_id}"
            )
        ])
    
    if show_selection:
        buttons.append([
            InlineKeyboardButton(text="✅ ГЕНЕРИРОВАТЬ ВЫБРАННЫЕ", callback_data="generate_selected"),
            InlineKeyboardButton(text="🗑️ ОЧИСТИТЬ ВЫБОР", callback_data="clear_selection")
        ])
    
    buttons.append([InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🔗 ГЕНЕРАТОР ССЫЛОК
class NFTLinkGenerator:
    
    @staticmethod
    def generate_nft_links(collection_id: str, count: int = 20) -> List[str]:
        """Генерирует реальные ссылки на NFT конкретной коллекции"""
        collection = NFT_GIFT_COLLECTIONS.get(collection_id)
        if not collection:
            return []
        
        links = []
        max_num = collection["max_number"]
        
        # Генерируем случайные номера
        if max_num < count:
            count = max_num
        
        numbers = random.sample(range(1, max_num + 1), count)
        
        for number in numbers:
            link = f"{collection['base_url']}{number}"
            links.append(link)
        
        return links

# 🤖 ОБРАБОТЧИКИ БОТА
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🎁 <b>NFT GIFT LINK GENERATOR</b>\n\n"
        "🔗 <b>Генерирует реальные ссылки на NFT Gifts</b>\n"
        "📊 <b>30 коллекций Telegram NFT</b>\n"
        "🎯 <b>Выбирайте несколько коллекций сразу</b>\n\n"
        "<i>Бот создает рабочие ссылки на NFT подарки</i>",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "generate_links")
async def on_generate_links(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔗 <b>ГЕНЕРАЦИЯ ССЫЛОК НА NFT GIFTS</b>\n\n"
        "🎯 Выберите коллекцию для генерации ссылок\n"
        "📊 Каждая ссылка ведет на реальный NFT\n"
        "🔄 Можно выбрать несколько коллекций\n\n"
        "<i>Нажмите на коллекцию для просмотра</i>",
        reply_markup=get_collections_keyboard(show_selection=False)
    )

@dp.callback_query(F.data.startswith("collection_"))
async def on_collection_selected(callback: CallbackQuery):
    collection_id = callback.data.replace("collection_", "")
    collection = NFT_GIFT_COLLECTIONS.get(collection_id)
    
    if not collection:
        await callback.answer("❌ Коллекция не найдена")
        return
    
    # Генерируем пример ссылок
    generator = NFTLinkGenerator()
    sample_links = generator.generate_nft_links(collection_id, 5)
    
    links_text = "\n".join([f"{i+1}. <a href='{link}'>{link}</a>" for i, link in enumerate(sample_links)])
    
    await callback.message.edit_text(
        f"🎁 <b>{collection['name']}</b>\n\n"
        f"📝 {collection.get('description', '')}\n"
        f"🔢 Всего NFT: {collection['max_number']:,}\n"
        f"🔗 Формат: {collection['base_url']}[номер]\n\n"
        f"<b>Примеры ссылок:</b>\n{links_text}\n\n"
        f"<i>Нажмите кнопку ниже для генерации ссылок</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 СГЕНЕРИРОВАТЬ 20 ССЫЛОК", callback_data=f"generate_{collection_id}")],
            [InlineKeyboardButton(text="✅ ВЫБРАТЬ КОЛЛЕКЦИЮ", callback_data=f"select_{collection_id}")],
            [InlineKeyboardButton(text="🎯 ВЫБРАТЬ ДРУГУЮ", callback_data="generate_links")]
        ]),
        disable_web_page_preview=True
    )

@dp.callback_query(F.data.startswith("generate_"))
async def on_generate_collection(callback: CallbackQuery):
    collection_id = callback.data.replace("generate_", "")
    collection = NFT_GIFT_COLLECTIONS.get(collection_id)
    
    if not collection:
        await callback.answer("❌ Коллекция не найдена")
        return
    
    await callback.message.edit_text(
        f"🔄 <b>ГЕНЕРАЦИЯ ССЫЛОК...</b>\n\n"
        f"🎁 Коллекция: {collection['name']}\n"
        f"🔢 Генерирую 20 случайных NFT ссылок\n"
        f"⏳ Ожидайте 3-5 секунд...",
    )
    
    # Генерируем ссылки
    generator = NFTLinkGenerator()
    links = generator.generate_nft_links(collection_id, 20)
    
    if not links:
        await callback.message.edit_text(
            f"❌ <b>ОШИБКА ГЕНЕРАЦИИ</b>\n\n"
            f"{collection['name']}\n"
            f"Не удалось сгенерировать ссылки",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Форматируем ссылки
    links_formatted = []
    for i, link in enumerate(links, 1):
        nft_id = link.split('-')[-1]
        links_formatted.append(f"{i:2d}. <a href='{link}'>NFT #{nft_id}</a>")
    
    links_text = "\n".join(links_formatted)
    
    # Сохраняем в историю
    generation_history.append({
        "collection": collection["name"],
        "count": len(links),
        "links": links[:5],  # Сохраняем только первые 5
        "timestamp": time.time()
    })
    
    result_text = (
        f"✅ <b>ССЫЛКИ СГЕНЕРИРОВАНЫ!</b>\n\n"
        f"🎁 <b>Коллекция:</b> {collection['name']}\n"
        f"🔗 <b>Сгенерировано:</b> {len(links)} ссылок\n"
        f"🔢 <b>Всего NFT в коллекции:</b> {collection['max_number']:,}\n\n"
        f"<b>СГЕНЕРИРОВАННЫЕ ССЫЛКИ:</b>\n{links_text}\n\n"
        f"<i>Нажмите на ссылку, чтобы открыть NFT</i>"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 СОХРАНИТЬ ССЫЛКИ", callback_data=f"save_{collection_id}")],
        [InlineKeyboardButton(text="🔄 ЕЩЁ 20 ССЫЛОК", callback_data=f"generate_{collection_id}")],
        [InlineKeyboardButton(text="🎯 ДРУГАЯ КОЛЛЕКЦИЯ", callback_data="generate_links")]
    ])
    
    await callback.message.edit_text(result_text, reply_markup=keyboard, disable_web_page_preview=True)

@dp.callback_query(F.data.startswith("select_"))
async def on_select_single(callback: CallbackQuery):
    collection_id = callback.data.replace("select_", "")
    
    if collection_id in selected_collections:
        selected_collections.remove(collection_id)
        action = "убрана"
    else:
        selected_collections.add(collection_id)
        action = "добавлена"
    
    collection = NFT_GIFT_COLLECTIONS[collection_id]
    await callback.answer(f"✅ {collection['name']} {action} в выбор")
    
    # Возвращаемся к списку коллекций
    await callback.message.edit_text(
        "🔗 <b>ГЕНЕРАЦИЯ ССЫЛОК НА NFT GIFTS</b>\n\n"
        f"✅ Выбрано: {len(selected_collections)}/30 коллекций\n"
        "🎯 Выберите коллекцию для генерации ссылок\n\n"
        "<i>Нажмите на коллекцию для просмотра</i>",
        reply_markup=get_collections_keyboard(show_selection=True)
    )

@dp.callback_query(F.data == "select_collections")
async def on_select_collections(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 <b>ВЫБОР КОЛЛЕКЦИЙ ДЛЯ МАССОВОЙ ГЕНЕРАЦИИ</b>\n\n"
        f"✅ Выбрано: {len(selected_collections)}/30 коллекций\n"
        "🖱️ Нажмите на коллекцию для выбора/отмены\n"
        "📊 Можно выбрать несколько коллекций\n\n"
        "<i>После выбора нажмите 'Генерировать выбранные'</i>",
        reply_markup=get_collections_keyboard(show_selection=True)
    )

@dp.callback_query(F.data == "clear_selection")
async def on_clear_selection(callback: CallbackQuery):
    selected_collections.clear()
    await callback.answer("✅ Выбор очищен")
    await callback.message.edit_text(
        "🎯 <b>ВЫБОР КОЛЛЕКЦИЙ ДЛЯ МАССОВОЙ ГЕНЕРАЦИИ</b>\n\n"
        "✅ Выбрано: 0/30 коллекций\n"
        "🖱️ Нажмите на коллекцию для выбора/отмены\n"
        "📊 Можно выбрать несколько коллекций\n\n"
        "<i>После выбора нажмите 'Генерировать выбранные'</i>",
        reply_markup=get_collections_keyboard(show_selection=True)
    )

@dp.callback_query(F.data == "generate_selected")
async def on_generate_selected(callback: CallbackQuery):
    if not selected_collections:
        await callback.answer("❌ Не выбрано ни одной коллекции")
        return
    
    collections_list = "\n".join([f"• {NFT_GIFT_COLLECTIONS[cid]['name']}" for cid in selected_collections])
    
    await callback.message.edit_text(
        f"🚀 <b>МАССОВАЯ ГЕНЕРАЦИЯ ССЫЛОК</b>\n\n"
        f"📊 Коллекций: {len(selected_collections)}\n"
        f"🔗 Будет сгенерировано: {len(selected_collections) * 15} ссылок\n"
        f"⏳ Время: ~{len(selected_collections) * 2} секунд\n\n"
        f"<b>Выбранные коллекции:</b>\n{collections_list}\n\n"
        f"<i>Начинаю генерацию...</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ НАЧАТЬ ГЕНЕРАЦИЮ", callback_data="start_mass_generation")],
            [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="select_collections")]
        ])
    )

@dp.callback_query(F.data == "start_mass_generation")
async def on_start_mass_generation(callback: CallbackQuery):
    if not selected_collections:
        await callback.answer("❌ Не выбрано коллекций")
        return
    
    await callback.message.edit_text(
        "🔄 <b>МАССОВАЯ ГЕНЕРАЦИЯ...</b>\n\n"
        "⏳ Генерирую ссылки для выбранных коллекций\n"
        "🔗 Создаю рабочие NFT ссылки\n"
        "⏱️ Ожидайте несколько секунд\n\n"
        "<i>Статус будет обновлен</i>"
    )
    
    all_links = []
    generator = NFTLinkGenerator()
    
    for idx, coll_id in enumerate(selected_collections, 1):
        collection = NFT_GIFT_COLLECTIONS[coll_id]
        
        # Генерируем по 10 ссылок на коллекцию
        links = generator.generate_nft_links(coll_id, 10)
        
        # Добавляем информацию о коллекции
        for link in links:
            nft_id = link.split('-')[-1]
            all_links.append({
                "collection": collection["name"],
                "url": link,
                "nft_id": nft_id
            })
        
        # Обновляем статус
        status_text = (
            f"📊 <b>ГЕНЕРАЦИЯ {idx}/{len(selected_collections)}</b>\n\n"
            f"🎁 Коллекция: {collection['name']}\n"
            f"✅ Сгенерировано: {len(links)} ссылок\n"
            f"🔄 Продолжаю генерацию...\n\n"
            f"<i>Ожидайте завершения</i>"
        )
        
        if idx < len(selected_collections):
            await callback.message.edit_text(status_text)
            await asyncio.sleep(0.5)
    
    # Перемешиваем ссылки
    random.shuffle(all_links)
    
    # Формируем результат
    if all_links:
        links_text = ""
        for i, link_data in enumerate(all_links[:30], 1):  # Показываем первые 30
            links_text += f"{i:2d}. <a href='{link_data['url']}'>{link_data['collection']} #{link_data['nft_id']}</a>\n"
        
        result_text = (
            f"✅ <b>МАССОВАЯ ГЕНЕРАЦИЯ ЗАВЕРШЕНА!</b>\n\n"
            f"📊 Коллекций: {len(selected_collections)}\n"
            f"🔗 Всего ссылок: {len(all_links)}\n"
            f"🎁 Уникальных NFT: {len(all_links)}\n\n"
            f"<b>СГЕНЕРИРОВАННЫЕ ССЫЛКИ:</b>\n{links_text}"
        )
        
        if len(all_links) > 30:
            result_text += f"\n\n... и ещё {len(all_links) - 30} ссылок"
        
        # Сохраняем в историю
        generation_history.append({
            "type": "mass_generation",
            "collections_count": len(selected_collections),
            "total_links": len(all_links),
            "collections": [NFT_GIFT_COLLECTIONS[cid]["name"] for cid in selected_collections],
            "timestamp": time.time()
        })
    else:
        result_text = (
            f"❌ <b>ОШИБКА ГЕНЕРАЦИИ</b>\n\n"
            f"📊 Коллекций: {len(selected_collections)}\n"
            f"🔗 Сгенерировано: 0 ссылок\n\n"
            f"<i>Попробуйте еще раз</i>"
        )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💾 СОХРАНИТЬ ВСЕ ССЫЛКИ", callback_data="save_all_links")],
        [InlineKeyboardButton(text="🔄 ПОВТОРИТЬ", callback_data="generate_selected")],
        [InlineKeyboardButton(text="🔙 В МЕНЮ", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(result_text, reply_markup=keyboard, disable_web_page_preview=True)

@dp.callback_query(F.data == "quick_generate")
async def on_quick_generate(callback: CallbackQuery):
    # Выбираем 5 случайных коллекций для быстрой генерации
    quick_collections = random.sample(list(NFT_GIFT_COLLECTIONS.keys()), 5)
    
    quick_text = "<b>⚡ БЫСТРАЯ ГЕНЕРАЦИЯ</b>\n\n"
    quick_text += "<b>Выбраны коллекции:</b>\n"
    
    buttons = []
    for coll_id in quick_collections:
        collection = NFT_GIFT_COLLECTIONS[coll_id]
        quick_text += f"• {collection['name']}\n"
        buttons.append([
            InlineKeyboardButton(
                text=f"🔗 {collection['name']}",
                callback_data=f"generate_{coll_id}"
            )
        ])
    
    quick_text += f"\n<i>Будет сгенерировано по 10 ссылок на коллекцию</i>"
    
    buttons.append([
        InlineKeyboardButton(text="🎲 СЛУЧАЙНЫЙ НАБОР", callback_data="quick_generate"),
        InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_main")
    ])
    
    await callback.message.edit_text(
        quick_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query(F.data == "show_history")
async def on_show_history(callback: CallbackQuery):
    if not generation_history:
        await callback.message.edit_text(
            "📭 <b>ИСТОРИЯ ПУСТА</b>\n\n"
            "Начните генерацию ссылок на NFT!",
            reply_markup=get_main_keyboard()
        )
        return
    
    history_text = "📊 <b>ИСТОРИЯ ГЕНЕРАЦИИ:</b>\n\n"
    
    for i, record in enumerate(reversed(generation_history[-8:]), 1):
        time_str = time.strftime('%H:%M', time.localtime(record.get('timestamp', time.time())))
        
        if record.get('type') == 'mass_generation':
            history_text += (
                f"{i}. ⚡ <b>Массовая генерация</b>\n"
                f"   📅 {time_str} | 📊 {record.get('collections_count', 0)} коллекций\n"
                f"   🔗 {record.get('total_links', 0)} ссылок\n"
            )
        else:
            history_text += (
                f"{i}. 🎁 <b>{record.get('collection', 'Unknown')}</b>\n"
                f"   📅 {time_str} | 🔗 {record.get('count', 0)} ссылок\n"
            )
    
    history_text += f"\n<i>Всего записей: {len(generation_history)}</i>"
    
    await callback.message.edit_text(
        history_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑️ ОЧИСТИТЬ ИСТОРИЮ", callback_data="clear_history")],
            [InlineKeyboardButton(text="💾 СОХРАНИТЬ ИСТОРИЮ", callback_data="save_history")],
            [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(F.data == "save_history")
async def on_save_history(callback: CallbackQuery):
    if not generation_history:
        await callback.answer("❌ Нет данных для сохранения")
        return
    
    import tempfile
    import os
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("🎁 NFT GIFT LINK GENERATOR - ИСТОРИЯ\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Дата экспорта: {time.ctime()}\n")
            f.write(f"Всего записей: {len(generation_history)}\n\n")
            
            for i, record in enumerate(reversed(generation_history), 1):
                f.write(f"\n{'='*40}\n")
                f.write(f"ЗАПИСЬ #{i}\n")
                f.write(f"{'='*40}\n\n")
                
                if record.get('type') == 'mass_generation':
                    f.write(f"Тип: Массовая генерация\n")
                    f.write(f"Коллекций: {record.get('collections_count', 0)}\n")
                    f.write(f"Ссылок: {record.get('total_links', 0)}\n")
                    f.write(f"Дата: {time.ctime(record.get('timestamp', time.time()))}\n")
                    
                    collections = record.get('collections', [])
                    if collections:
                        f.write("\nКоллекции:\n")
                        for coll in collections:
                            f.write(f"  • {coll}\n")
                else:
                    f.write(f"Коллекция: {record.get('collection', 'Unknown')}\n")
                    f.write(f"Ссылок: {record.get('count', 0)}\n")
                    f.write(f"Дата: {time.ctime(record.get('timestamp', time.time()))}\n")
                    
                    links = record.get('links', [])
                    if links:
                        f.write("\nСсылки:\n")
                        for link in links:
                            f.write(f"  • {link}\n")
                
                f.write("\n")
            
            filename = f.name
        
        document = FSInputFile(filename)
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=document,
            caption="📁 <b>История генерации сохранена</b>"
        )
        
        await callback.answer("✅ Файл отправлен")
        os.unlink(filename)
        
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")
        await callback.answer("❌ Ошибка сохранения")

@dp.callback_query(F.data.startswith("save_"))
async def on_save_links(callback: CallbackQuery):
    collection_id = callback.data.replace("save_", "")
    
    # Ищем последнюю генерацию для этой коллекции
    links_to_save = []
    collection_name = ""
    
    for record in reversed(generation_history):
        if record.get('collection') == NFT_GIFT_COLLECTIONS.get(collection_id, {}).get('name'):
            links_to_save = record.get('links', [])
            collection_name = record.get('collection', 'Unknown')
            break
    
    if not links_to_save:
        await callback.answer("❌ Нет ссылок для сохранения")
        return
    
    import tempfile
    import os
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(f"🎁 NFT GIFT LINKS - {collection_name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Коллекция: {collection_name}\n")
            f.write(f"Дата: {time.ctime()}\n")
            f.write(f"Всего ссылок: {len(links_to_save)}\n\n")
            f.write("ССЫЛКИ:\n\n")
            
            for i, link in enumerate(links_to_save, 1):
                f.write(f"{i:3d}. {link}\n")
            
            filename = f.name
        
        document = FSInputFile(filename)
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=document,
            caption=f"📁 <b>Ссылки на {collection_name} сохранены</b>"
        )
        
        await callback.answer("✅ Файл отправлен")
        os.unlink(filename)
        
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")
        await callback.answer("❌ Ошибка сохранения")

@dp.callback_query(F.data == "save_all_links")
async def on_save_all_links(callback: CallbackQuery):
    if not selected_collections:
        await callback.answer("❌ Не выбрано коллекций")
        return
    
    # Генерируем ссылки заново
    generator = NFTLinkGenerator()
    all_links_data = []
    
    for coll_id in selected_collections:
        links = generator.generate_nft_links(coll_id, 10)
        collection = NFT_GIFT_COLLECTIONS[coll_id]
        
        for link in links:
            nft_id = link.split('-')[-1]
            all_links_data.append({
                "collection": collection["name"],
                "url": link,
                "nft_id": nft_id
            })
    
    if not all_links_data:
        await callback.answer("❌ Не удалось сгенерировать ссылки")
        return
    
    import tempfile
    import os
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("🎁 NFT GIFT LINKS - МАССОВАЯ ГЕНЕРАЦИЯ\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Коллекций: {len(selected_collections)}\n")
            f.write(f"Всего ссылок: {len(all_links_data)}\n")
            f.write(f"Дата: {time.ctime()}\n\n")
            
            f.write("КОЛЛЕКЦИИ:\n")
            for coll_id in selected_collections:
                f.write(f"• {NFT_GIFT_COLLECTIONS[coll_id]['name']}\n")
            
            f.write("\n" + "=" * 60 + "\n\n")
            f.write("ВСЕ ССЫЛКИ:\n\n")
            
            for i, link_data in enumerate(all_links_data, 1):
                f.write(f"{i:4d}. {link_data['collection']} - {link_data['url']}\n")
            
            filename = f.name
        
        document = FSInputFile(filename)
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=document,
            caption="📁 <b>Все ссылки массовой генерации сохранены</b>"
        )
        
        await callback.answer("✅ Файл отправлен")
        os.unlink(filename)
        
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")
        await callback.answer("❌ Ошибка сохранения")

@dp.callback_query(F.data == "clear_history")
async def on_clear_history(callback: CallbackQuery):
    generation_history.clear()
    await callback.message.edit_text(
        "✅ <b>История очищена!</b>",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "info")
async def on_info(callback: CallbackQuery):
    total_nfts = sum(c['max_number'] for c in NFT_GIFT_COLLECTIONS.values())
    
    info_text = (
        "ℹ️ <b>ИНФОРМАЦИЯ О БОТЕ</b>\n\n"
        "🎁 <b>NFT GIFT LINK GENERATOR</b>\n\n"
        "🔗 <b>Что делает бот:</b>\n"
        "• Генерирует рабочие ссылки на NFT Gifts\n"
        "• Поддерживает 30 коллекций Telegram\n"
        "• Можно выбирать несколько коллекций\n"
        "• Сохраняет историю генерации\n\n"
        "📊 <b>Статистика:</b>\n"
        f"• Коллекций: {len(NFT_GIFT_COLLECTIONS)}\n"
        f"• NFT всего: {total_nfts:,}\n"
        f"• История: {len(generation_history)} записей\n"
        f"• Выбрано: {len(selected_collections)} коллекций\n\n"
        "💡 <b>Как использовать:</b>\n"
        "1. Выберите коллекцию\n"
        "2. Нажмите 'Сгенерировать ссылки'\n"
        "3. Откройте ссылку в Telegram\n"
        "4. Посмотрите информацию о NFT\n\n"
        "<i>Все ссылки рабочие и ведут на реальные NFT</i>"
    )
    
    await callback.message.edit_text(
        info_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 НАЧАТЬ ГЕНЕРАЦИЮ", callback_data="generate_links")],
            [InlineKeyboardButton(text="🔙 НАЗАД", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(F.data == "back_to_main")
async def on_back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎁 <b>NFT GIFT LINK GENERATOR</b>\n\n"
        "🔗 <b>Генерирует реальные ссылки на NFT Gifts</b>\n"
        "📊 <b>30 коллекций Telegram NFT</b>\n"
        "🎯 <b>Выбирайте несколько коллекций сразу</b>\n\n"
        "<i>Бот создает рабочие ссылки на NFT подарки</i>",
        reply_markup=get_main_keyboard()
    )

@dp.message()
async def handle_unknown(message: Message):
    await message.answer(
        "🎁 <b>NFT GIFT LINK GENERATOR</b>\n\n"
        "Используйте кнопки меню или команду /start",
        reply_markup=get_main_keyboard()
    )

# 🚀 ЗАПУСК БОТА НА Render
async def on_startup(bot: Bot):
    """Функция, которая выполняется при старте бота"""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logger.info(f"✅ Бот запущен: @{me.username}")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")

# Настройка веб-сервера для Render
def main():
    # Получаем порт из переменной окружения Render (по умолчанию 10000)
    port = int(os.environ.get("PORT", 10000))
    
    # Регистрируем функцию on_startup
    dp.startup.register(on_startup)
    
    # Создаем веб-приложение aiohttp
    app = web.Application()
    
    # Создаем обработчик вебхуков для Telegram
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    
    # Регистрируем маршрут для вебхука
    # Все обновления от Telegram будут приходить на /webhook
    webhook_handler.register(app, path="/webhook")
    
    # Настраиваем приложение aiogram
    setup_application(app, dp, bot=bot)
    
    # Запускаем веб-сервер
    # Важно: слушаем на 0.0.0.0 чтобы принимать запросы извне
    logger.info(f"🚀 Запускаю веб-сервер на порту {port}")
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
