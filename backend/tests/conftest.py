import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:test@localhost:5432/kkeugi_test",
)
os.environ.setdefault("JWT_SECRET", "test-secret-not-for-prod-only-for-pytest-32b")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-client-id.apps.googleusercontent.com")

from app.db.base import Base  # noqa: E402
from app.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.users import models as users_models  # noqa: F401, E402


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(os.environ["DATABASE_URL"], poolclass=None)
    async with engine.begin() as conn:
        # DROP SCHEMA CASCADE — alembic이 만든 테이블 (FK 참조 포함)까지
        # 모두 제거. Base.metadata.drop_all은 ORM 모델 (users·refresh_tokens)만
        # 알아서 FK 의존성으로 실패함. CI는 alembic upgrade를 test DB에 먼저
        # 돌리므로 9개 테이블이 존재 → CASCADE 리셋 필수.
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    maker = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def fake_google_identity(monkeypatch):
    from app.auth.google import GoogleIdentity

    def _verify(token: str) -> GoogleIdentity:
        return GoogleIdentity(
            sub=f"google-sub-{token}",
            email=f"user-{token}@example.com",
            name=f"Test User {token}",
            email_verified=True,
        )

    monkeypatch.setattr("app.auth.routes.verify_google_id_token", _verify)
