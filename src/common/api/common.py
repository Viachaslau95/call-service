from fastapi import APIRouter

router = APIRouter(tags=['Common'])


@router.get('/healthcheck')
async def healthcheck() -> str:
    return 'OK'