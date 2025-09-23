import uvicorn

from src.config import config

if __name__ == '__main__':
    uvicorn.run('src.app:create_app', port=config.api_port, host=config.api_host, reload=True)
