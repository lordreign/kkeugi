from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.routes import router as auth_router
from app.channels.routes import router as fcm_router
from app.config import get_settings
from app.feature_flags import router as feature_flags_router
from app.health.routes import router as health_router
from app.payments.routes import router as payments_router
from app.reports.routes import router as reports_router
from app.telegram.routes import me_router as telegram_me_router
from app.telegram.routes import webhook_router as telegram_webhook_router
from app.thresholds.routes import router as thresholds_router
from app.usage.routes import router as usage_router
from app.users.routes import router as users_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # test 환경(pytest)에서는 스케줄러 미가동
    if settings.environment != "test":
        from app.scheduler import shutdown_scheduler, start_scheduler

        start_scheduler()
        yield
        shutdown_scheduler()
    else:
        yield


app = FastAPI(
    title="끊기 (Kkeugi) API",
    version="0.1.0",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(usage_router)
app.include_router(telegram_me_router)
app.include_router(telegram_webhook_router)
app.include_router(payments_router)
app.include_router(reports_router)
app.include_router(fcm_router)
app.include_router(thresholds_router)
app.include_router(feature_flags_router)

if settings.environment in ("development", "test"):
    from app.auth.dev import router as dev_auth_router

    app.include_router(dev_auth_router)


# Unhandled 5xx 에러를 Telegram 운영자 chat 으로 알림 (Sentry 대체).
# fingerprint 단위 5분 cooldown 으로 spam 방지. 알림 실패가 응답을 막지 않음.
@app.exception_handler(Exception)
async def _unhandled_exception_to_telegram(request: Request, exc: Exception):
    from app.observability.error_notifier import notify_exception

    user_email = None
    user_id = None
    # request.state.user 가 인증 dependency 에서 세팅돼 있으면 활용
    user = getattr(request.state, "user", None)
    if user is not None:
        user_email = getattr(user, "email", None)
        user_id = str(getattr(user, "id", "")) or None

    await notify_exception(
        exc,
        path=f"{request.method} {request.url.path}",
        user_email=user_email,
        user_id=user_id,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# dev/test 환경에서만 — 알림 검증용 boom endpoint.
if settings.environment in ("development", "test"):

    @app.get("/v1/_dev/boom")
    async def _dev_boom() -> dict:
        """의도적 ZeroDivisionError 발생 — error_notifier 검증용."""
        return {"answer": 1 / 0}  # noqa: B018
