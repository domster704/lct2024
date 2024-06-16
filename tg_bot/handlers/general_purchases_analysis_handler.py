"""
Раздел <Общий анализ закупок>
"""
import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import KeyboardButton, Message, BufferedInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.config import bot, apiURL_ML
from tg_bot.db.db import User
from tg_bot.db.db_utils import getUser
from tg_bot.res.action_list_text import COMMON_ANALYSIS_BUTTON_TEXT
from tg_bot.res.general_purchases_analysis_text import *
from tg_bot.res.general_text import *
from tg_bot.state.app_state import AppState
from tg_bot.state.general_purchase_analysis_state import CommonPurchaseAnalysisState
from tg_bot.utils import base64ToBufferInputStream


class GeneralPurchaseAnalysis(object):
    @staticmethod
    async def allStatistics(message: Message, period, price):
        user: User = await getUser(message.chat.id)
        async with aiohttp.ClientSession(cookies=user.cookies) as session:
            async with session.get(f"{apiURL_ML}/api/v1/ml/analytics_all/purchase_stats", params={
                "period": period,
                "summa": str(price),
            }) as r:
                res = await r.json()
                print(res)
                if res['state'] != 'Success':
                    return b''

                return base64ToBufferInputStream(res['plot_image'])

    @staticmethod
    async def allHistoryAnalysis(message: Message):
        user: User = await getUser(message.chat.id)
        async with aiohttp.ClientSession(cookies=user.cookies) as session:
            async with session.get(f"{apiURL_ML}/api/v1/ml/analytics_all/history", params={
                "n": 15,
            }) as r:
                res = await r.json()
                print(res)
                if r.status != 200:
                    return b''

                return base64ToBufferInputStream(res['file'])


commonPurchasesAnalysisRouter = Router()


@commonPurchasesAnalysisRouter.message(default_state, F.text == COMMON_ANALYSIS_BUTTON_TEXT,
                                       flags={"rights": "analysis_common"})
@commonPurchasesAnalysisRouter.message(AppState.actionList, F.text == COMMON_ANALYSIS_BUTTON_TEXT,
                                       flags={"rights": "analysis_common"})
@commonPurchasesAnalysisRouter.message(AppState.commonPurchaseAnalysis, F.text == COMMON_ANALYSIS_BUTTON_TEXT,
                                       flags={"rights": "analysis_common"})
async def commonPurchaseAnalysisInit(message: Message, state: FSMContext) -> None:
    await state.set_state(AppState.commonPurchaseAnalysis)

    keyboard = ReplyKeyboardBuilder().row(
        KeyboardButton(text=PURCHASES_STATISTIC_BUTTON_TEXT),
        KeyboardButton(text=TOP_EXPENSIVE_BUTTON_TEXT)
    ).row(
        KeyboardButton(text=BACK_BUTTON_TEXT)
    )
    print(await state.get_state())
    await message.answer(text=COMMON_PURCHASES_STATISTIC_HELLO_TEXT,
                         reply_markup=keyboard.as_markup(resize_keyboard=True))


@commonPurchasesAnalysisRouter.message(AppState.commonPurchaseAnalysis, F.text == PURCHASES_STATISTIC_BUTTON_TEXT)
async def purchaseStatistics(message: Message, state: FSMContext) -> None:
    allHistoryAnalysis = await GeneralPurchaseAnalysis.allHistoryAnalysis(message)

    await bot.send_document(message.chat.id,
                            document=BufferedInputFile(allHistoryAnalysis, filename="all_history.xlsx"))


@commonPurchasesAnalysisRouter.message(AppState.commonPurchaseAnalysis, F.text == TOP_EXPENSIVE_BUTTON_TEXT)
async def suggestProduct(message: Message, state: FSMContext) -> None:
    keyboard = ReplyKeyboardBuilder().row(
        KeyboardButton(text=YEAR_TEXT),
        KeyboardButton(text=QUARTER_TEXT),
        KeyboardButton(text=MONTH_TEXT),
    ).row(
        KeyboardButton(text=BACK_BUTTON_TEXT)
    )

    await state.set_state(CommonPurchaseAnalysisState.choosePeriod)
    await message.answer(text=CHOSE_PERIOD_TEXT, reply_markup=keyboard.as_markup(resize_keyboard=True))


@commonPurchasesAnalysisRouter.message(CommonPurchaseAnalysisState.choosePeriod, F.text == YEAR_TEXT)
@commonPurchasesAnalysisRouter.message(CommonPurchaseAnalysisState.choosePeriod, F.text == QUARTER_TEXT)
@commonPurchasesAnalysisRouter.message(CommonPurchaseAnalysisState.choosePeriod, F.text == MONTH_TEXT)
async def suggestProductYear(message: Message, state: FSMContext) -> None:
    await state.set_state(CommonPurchaseAnalysisState.chooseStatisticType)

    keyboard = ReplyKeyboardBuilder().add(
        KeyboardButton(text=AMOUNT_OF_PURCHASES_BUTTON_TEXT),
        KeyboardButton(text=PRICE_OF_PURCHASES_BUTTON_TEXT),
    ).row(
        KeyboardButton(text=BACK_BUTTON_TEXT)
    )

    period: int = 0
    if message.text == YEAR_TEXT:
        period = 1
    elif message.text == QUARTER_TEXT:
        period = 2
    elif message.text == MONTH_TEXT:
        period = 3

    await state.update_data(allPurchaseAnalysis_period=period)
    await message.answer(text=CHOSE_TYPE_TEXT, reply_markup=keyboard.as_markup(resize_keyboard=True))


@commonPurchasesAnalysisRouter.message(CommonPurchaseAnalysisState.chooseStatisticType,
                                       F.text == AMOUNT_OF_PURCHASES_BUTTON_TEXT)
async def suggestProductYear(message: Message, state: FSMContext) -> None:
    period: int = (await state.get_data())['allPurchaseAnalysis_period']
    allStatisticsAmount = await GeneralPurchaseAnalysis.allStatistics(message, period, False)

    await bot.send_photo(message.chat.id,
                         photo=BufferedInputFile(allStatisticsAmount, filename="amount.png"))


@commonPurchasesAnalysisRouter.message(CommonPurchaseAnalysisState.chooseStatisticType,
                                       F.text == PRICE_OF_PURCHASES_BUTTON_TEXT)
async def suggestProductYear(message: Message, state: FSMContext) -> None:
    period: int = (await state.get_data())['allPurchaseAnalysis_period']
    allStatisticsPrice = await GeneralPurchaseAnalysis.allStatistics(message, period, True)

    await bot.send_photo(message.chat.id,
                         photo=BufferedInputFile(allStatisticsPrice, filename="price.png"))
