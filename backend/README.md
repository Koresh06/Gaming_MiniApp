

uvicorn src.presentation.api.main:create_app --host 0.0.0.0 --port 8000 --factory


python -m src.infrastructure.telegram.bot.main