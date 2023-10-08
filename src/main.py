import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=True,
        reload_dirs=["/app"],
    )
