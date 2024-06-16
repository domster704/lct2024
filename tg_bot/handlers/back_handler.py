"""
Раздел с кнопками Назад для возврата на предыдущий шаг/этап
"""

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from tg_bot.handlers.actions_list_handler import actionListHandlerInit
from tg_bot.handlers.choose_purchase import choosePurchaseInit, choosePurchaseActionList
from tg_bot.handlers.general_purchases_analysis_handler import commonPurchaseAnalysisInit
from tg_bot.handlers.info_handler import infoHandlerInit
from tg_bot.handlers.product_handler import productInit, productActionsInit, enterProductName
from tg_bot.res.general_text import BACK_BUTTON_TEXT
from tg_bot.state.app_state import AppState
from tg_bot.state.choose_purchase_state import ChoosePurchaseState
from tg_bot.state.create_new_purchase_state import CreateNewPurchaseState
from tg_bot.state.general_purchase_analysis_state import CommonPurchaseAnalysisState
from tg_bot.state.info_state import InfoState
from tg_bot.state.product_state import ProductState

backRouter = Router()


@backRouter.message(default_state, F.text == BACK_BUTTON_TEXT)
@backRouter.message(InfoState.userInfo, F.text == BACK_BUTTON_TEXT)
@backRouter.message(AppState.info, F.text == BACK_BUTTON_TEXT)
async def backActionUserInfo(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Информация о пользователе и помощь>.
    Используется по умолчанию, если есть только default_state
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.info)
    await infoHandlerInit(message, state)


@backRouter.message(AppState.actionList, F.text == BACK_BUTTON_TEXT)
async def backButtonActionList(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Список основных действий>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.info)
    await infoHandlerInit(message, state)


@backRouter.message(AppState.commonPurchaseAnalysis, F.text == BACK_BUTTON_TEXT)
async def backButtonGeneralPurchaseAnalysis(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Общий анализ закупок>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await actionListHandlerInit(message, state)


@backRouter.message(AppState.balanceState, F.text == BACK_BUTTON_TEXT)
async def backButtonBalance(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Общий анализ закупок>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await actionListHandlerInit(message, state)


@backRouter.message(ProductState.productName, F.text == BACK_BUTTON_TEXT)
async def backButtonProductName(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Товар>:`ввод имени товара`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await actionListHandlerInit(message, state)


@backRouter.message(ProductState.productNameSuggestedList, F.text == BACK_BUTTON_TEXT)
@backRouter.message(ProductState.enterProductNumFromList, F.text == BACK_BUTTON_TEXT)
async def backButtonProductSuggestedList(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Товар>:`список товаров с пагинацией`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.product)
    await productInit(message, state)


@backRouter.message(ProductState.productWaitActions, F.text == BACK_BUTTON_TEXT)
@backRouter.message(ProductState.productActions, F.text == BACK_BUTTON_TEXT)
async def backButtonPagination(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Товар>:`список товаров с пагинацией`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(ProductState.productName)
    await productInit(message, state)


@backRouter.message(ProductState.choosePeriod, F.text == BACK_BUTTON_TEXT)
async def backButtonProductActions(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Товар>:`список действий с товаром`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(ProductState.productNameSuggestedList)
    await productActionsInit(message, state)


@backRouter.message(ProductState.productNameSuggestedList, F.text == BACK_BUTTON_TEXT)
async def backButtonSuggestedList(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Товар>:`список действий с товаром`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(ProductState.productName)
    await enterProductName(message, state)


@backRouter.message(AppState.productAnalysis, F.text == BACK_BUTTON_TEXT)
async def backButtonProductAnalysis(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Аналитика по товару>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(ProductState.productActions)
    await productActionsInit(message, state)


@backRouter.message(ProductState.waitPurchaseActions, F.text == BACK_BUTTON_TEXT)
async def backButtonPurchaseActions(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Закупка>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(ProductState.productActions)
    await productActionsInit(message, state)


@backRouter.message(AppState.activePurchase, F.text == BACK_BUTTON_TEXT)
@backRouter.message(ChoosePurchaseState.purchaseList, F.text == BACK_BUTTON_TEXT)
@backRouter.message(ChoosePurchaseState.choosePurchase, F.text == BACK_BUTTON_TEXT)
async def backButtonActivePurchase(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Выбор закупки>
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await actionListHandlerInit(message, state)


@backRouter.message(ChoosePurchaseState.editPurchase, F.text == BACK_BUTTON_TEXT)
async def backButtonEditActivePurchase(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Выбор закупки>:`редактировать закупку`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await choosePurchaseInit(message, state)


@backRouter.message(AppState.createNewPurchase, F.text == BACK_BUTTON_TEXT)
@backRouter.message(CreateNewPurchaseState.id, F.text == BACK_BUTTON_TEXT)
@backRouter.message(CreateNewPurchaseState.lotId, F.text == BACK_BUTTON_TEXT)
@backRouter.message(CreateNewPurchaseState.customerId, F.text == BACK_BUTTON_TEXT)
async def backButtonCreateNewPurchase(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Создание новой закупки>:
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await actionListHandlerInit(message, state)


@backRouter.message(CommonPurchaseAnalysisState.choosePeriod, F.text == BACK_BUTTON_TEXT)
async def backButtonCommonPurchaseAnalysis(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Создание новой закупки>:
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await commonPurchaseAnalysisInit(message, state)


@backRouter.message(ChoosePurchaseState.chooseActionsFromList, F.text == BACK_BUTTON_TEXT)
@backRouter.message(ProductState.initActions, F.text == BACK_BUTTON_TEXT)
async def backButtonEditPurchase(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Редактирование закупки>:
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await choosePurchaseActionList(message, state)


@backRouter.message(ProductState.productStatisticChoosePeriod, F.text == BACK_BUTTON_TEXT)
async def backButtonProductStatistics(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Статистика товара>:
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await productActionsInit(message, state)


@backRouter.message(CommonPurchaseAnalysisState.chooseStatisticType, F.text == BACK_BUTTON_TEXT)
async def backButtonProductStatistics(message: Message, state: FSMContext) -> None:
    """
    Кнопка назад в блоке <Общий анализ>:`выбор типа графика`
    :param message:
    :param state:
    :return:
    """
    await state.set_state(AppState.actionList)
    await commonPurchaseAnalysisInit(message, state)
