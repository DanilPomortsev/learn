import uvicorn
from settings import settings_
#запускаем сервер с базовыми настройками
if __name__ == "__main__":
    uvicorn.run(
        "app_:app",
        host=settings_.server_host,
        port=settings_.server_port
    )