

uvicorn src.presentation.api.main:create_app --host 0.0.0.0 --port 8060 --factory --reload


python -m src.infrastructure.telegram.bot.main