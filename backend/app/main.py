from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.auth.routes import router as auth_router
from app.channels.routes import router as fcm_router
from app.config import get_settings
from app.health.routes import router as health_router
from app.payments.routes import router as payments_router
from app.reports.routes import router as reports_router
from app.telegram.routes import me_router as telegram_me_router
from app.telegram.routes import webhook_router as telegram_webhook_router
from app.thresholds.routes import router as thresholds_router
from app.usage.routes import router as usage_router
from app.users.routes import router as users_router

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=0.05,
        integrations=[FastApiIntegration()],
    )

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

if settings.environment in ("development", "test"):
    from app.auth.dev import router as dev_auth_router

    app.include_router(dev_auth_router)
