import logging
from uuid import UUID
from aiogram import Router, F, Bot
from aiogram.types import Message, PreCheckoutQuery
from aiogram.filters import CommandObject, Command
from dishka.integrations.aiogram import FromDishka

from src.core.mediator.mediator import Mediator
from src.application.exceptions.bet import BetAlreadyPaid
from src.domain.value_object.bet_status import BetStatus
from src.application.use_cases.bet.update import UpdateBetStatusRequest


logger = logging.getLogger(__name__)

router = Router()

@router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    logger.warning(
        "🔥 PRE_CHECKOUT_QUERY RECEIVED",
        extra={
            "id": query.id,
            "from": query.from_user.id,
            "currency": query.currency,
            "amount": query.total_amount,
        }
    )
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, mediator: FromDishka[Mediator],):
    payment = message.successful_payment

    if payment.currency != "XTR":
        return

    request = UpdateBetStatusRequest(
        bet_uuid=UUID(payment.invoice_payload),
        status=BetStatus.PAID,
        telegram_transaction_id=payment.telegram_payment_charge_id,
    )

    logger.info(
        "Получен successful_payment",
        extra={
            "bet_uuid": str(request.bet_uuid),
            "telegram_transaction_id": request.telegram_transaction_id,
            "amount": payment.total_amount,
        }
    )

    try:
        await mediator.handle(request)
    except BetAlreadyPaid:
        logger.info(
            "Ставка уже была оплачена, повторный callback",
            extra={"bet_uuid": str(request.bet_uuid)},
        )

    logger.info(
        "Ставка успешно переведена в PAID",
        extra={"bet_uuid": str(request.bet_uuid)},
    )


# @router.message(Command("refundStarPayment"))
# async def refund_handler(message: Message, command: CommandObject, bot: Bot):
#     if not command.args:
#         await message.answer(" Укажите ID транзакции")
#         return
    
#     transaction_id = command.args
    
#     try:
#         await bot.refund_star_payment(
#             user_id=message.from_user.id,
#             telegram_payment_charge_id=transaction_id
#         )
#         await message.answer(f" Возврат по транзакции {transaction_id} выполнен успешно")
#     except Exception as e:
#         await message.answer(f" Ошибка возврата: {str(e)}")