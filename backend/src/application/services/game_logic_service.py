import logging
import random
import secrets

from src.domain.entities.game_outcome_setting import GameOutcomeSetting


logger = logging.getLogger(__name__)


class GameLogicService:
    """
    Сервис игровой логики:
    - проверка корректности сумм вероятностей
    - выбор исхода игры на основе вероятностей
    - расчет суммы выигрыша
    - генерация seed для анимации (детерминируемая визуализация)
    """

    @staticmethod
    def validate_probabilities(outcomes: list[GameOutcomeSetting]) -> None:
        logger.debug(
            "Проверка корректности сумм вероятностей для игры",
            extra={
                "outcomes": [
                    {
                        "outcome_code": o.outcome_code.value,
                        "probability": o.probability,
                    }
                    for o in outcomes
                ]
            }
        )

        total = sum(o.probability for o in outcomes)

        if abs(total - 1) > 0.0001:
            logger.error(
                "Сумма вероятностей некорректна",
                extra={
                    "total_probability": total,
                    "allowed": 1.0,
                }
            )
            raise ValueError(f"Sum of probabilities must be 1, got: {total}")

        logger.info(
            "Вероятности успешно проверены",
            extra={"total_probability": total}
        )

    @staticmethod
    def choose_outcome(outcomes: list[GameOutcomeSetting]) -> GameOutcomeSetting:
        logger.debug(
            "Выбор исхода игры на основе вероятностей",
            extra={
                "weights": [
                    {"code": o.outcome_code.value, "prob": o.probability}
                    for o in outcomes
                ]
            }
        )

        probabilities = [o.probability for o in outcomes]
        selected = random.choices(outcomes, weights=probabilities, k=1)[0]

        logger.info(
            "Исход игры выбран",
            extra={
                "selected_outcome_code": selected.outcome_code.value,
                "probability": selected.probability,
                "multiplier": selected.multiplier,
            }
        )

        return selected

    @staticmethod
    def calculate_win_amount(bet_amount: int, outcome: GameOutcomeSetting) -> int:
        win = int(bet_amount * outcome.multiplier)

        logger.info(
            "Вычисление суммы выигрыша",
            extra={
                "bet_amount": bet_amount,
                "outcome_code": outcome.outcome_code.value,
                "multiplier": outcome.multiplier,
                "calculated_win": win,
            }
        )

        return win

    @staticmethod
    def generate_seed() -> str:
        seed = secrets.token_hex(16)

        logger.debug(
            "Сгенерирован seed для анимации",
            extra={"seed": seed}
        )

        return seed
