from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.init_db import init_db
from app.routers import all_routers, default_prefix

import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # 앱 시작 시 테이블 자동 생성
    yield

# Fast API 초기화시 swagger 자동 생성
app = FastAPI(
    title="공통코드 API",
    lifespan=lifespan,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)

for router in all_routers:
    app.include_router(router["router"], prefix=router.get("prefix", default_prefix))

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "공통코드 API 서버 정상 동작 중"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")