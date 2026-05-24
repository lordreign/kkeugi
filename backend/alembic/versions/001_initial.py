"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-24

users + refresh_tokens + usage_events (monthly partitioned) +
usage_event_dedupe + channel_subscriptions + fcm_tokens + thresholds +
weekly_reports + subscriptions
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID

revision: str = "001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # users
    op.create_table(
        "users",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("google_sub", sa.String(255), nullable=False, unique=True),
        sa.Column("kakao_id", sa.String(255), nullable=True, unique=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=True),
        sa.Column("tier", sa.String(20), nullable=False, server_default="free"),
        sa.Column("hourly_value", sa.Integer, nullable=True),
        sa.Column("work_start_hour", sa.SmallInteger, nullable=True),
        sa.Column("work_end_hour", sa.SmallInteger, nullable=True),
        sa.Column("timezone", sa.String(50), nullable=False, server_default="Asia/Seoul"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "tier IN ('free', 'one_time', 'subscription')", name="users_tier_check",
        ),
    )
    op.create_index("idx_users_google_sub", "users", ["google_sub"])
    op.create_index(
        "idx_users_kakao_id",
        "users",
        ["kakao_id"],
        postgresql_where=sa.text("kakao_id IS NOT NULL"),
    )
    op.create_index(
        "idx_users_tier_active",
        "users",
        ["tier"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # refresh_tokens
    op.create_table(
        "refresh_tokens",
        sa.Column("jti", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "issued_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "rotated_to",
            UUID(as_uuid=True),
            sa.ForeignKey("refresh_tokens.jti"),
            nullable=True,
        ),
        sa.Column("user_agent", sa.String(255), nullable=True),
        sa.Column("ip_address", INET, nullable=True),
    )
    op.create_index(
        "idx_refresh_tokens_user_active",
        "refresh_tokens",
        ["user_id"],
        postgresql_where=sa.text("revoked_at IS NULL"),
    )
    op.create_index(
        "idx_refresh_tokens_expires",
        "refresh_tokens",
        ["expires_at"],
        postgresql_where=sa.text("revoked_at IS NULL"),
    )

    # usage_events (monthly partitioned by occurred_at)
    op.execute(
        """
        CREATE TABLE usage_events (
            id UUID NOT NULL DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL,
            package_name VARCHAR(255) NOT NULL,
            category VARCHAR(20) NOT NULL,
            duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
            occurred_at TIMESTAMPTZ NOT NULL,
            in_work_hours BOOLEAN NOT NULL DEFAULT FALSE,
            source VARCHAR(20) NOT NULL DEFAULT 'usagestats',
            client_event_id UUID NOT NULL,
            synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (id, occurred_at),
            CONSTRAINT usage_events_category_check
              CHECK (category IN ('sns', 'shorts', 'game', 'webtoon', 'other')),
            CONSTRAINT usage_events_source_check
              CHECK (source IN ('usagestats', 'manual'))
        ) PARTITION BY RANGE (occurred_at)
        """,
    )
    op.create_index(
        "idx_usage_events_user_occurred",
        "usage_events",
        ["user_id", sa.text("occurred_at DESC")],
    )

    # initial 6 monthly partitions (2026-06 ~ 2026-12)
    for year, month in [(2026, m) for m in range(6, 13)]:
        next_y, next_m = (year, month + 1) if month < 12 else (year + 1, 1)
        op.execute(
            f"""
            CREATE TABLE usage_events_y{year}m{month:02d}
            PARTITION OF usage_events
            FOR VALUES FROM ('{year}-{month:02d}-01')
                        TO ('{next_y}-{next_m:02d}-01')
            """,
        )

    # usage_event_dedupe (non-partitioned, 24h TTL via daily cleanup cron)
    op.create_table(
        "usage_event_dedupe",
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("client_event_id", UUID(as_uuid=True), nullable=False),
        sa.Column(
            "inserted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("user_id", "client_event_id"),
    )
    op.create_index(
        "idx_usage_event_dedupe_inserted_at",
        "usage_event_dedupe",
        ["inserted_at"],
    )

    # channel_subscriptions (FCM / email / telegram / discord / slack)
    op.create_table(
        "channel_subscriptions",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("channel_identifier", sa.String(500), nullable=False),
        sa.Column("subscribed", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column(
            "preferred_send_hour", sa.SmallInteger, nullable=False, server_default="22",
        ),
        sa.Column(
            "subscribed_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("unsubscribed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", JSONB, nullable=True),
        sa.CheckConstraint(
            "channel IN ('fcm', 'email', 'telegram', 'discord', 'slack')",
            name="channel_subscriptions_channel_check",
        ),
        sa.UniqueConstraint("user_id", "channel", name="uq_channel_subs_user_channel"),
    )
    op.create_index(
        "idx_channel_subscriptions_active",
        "channel_subscriptions",
        ["user_id"],
        postgresql_where=sa.text("subscribed = TRUE"),
    )

    # fcm_tokens
    op.create_table(
        "fcm_tokens",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token", sa.String(1024), nullable=False, unique=True),
        sa.Column("device_id", sa.String(100), nullable=True),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("idx_fcm_tokens_user", "fcm_tokens", ["user_id"])

    # thresholds
    op.create_table(
        "thresholds",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("category", sa.String(20), nullable=False),
        sa.Column(
            "daily_limit_minutes",
            sa.Integer,
            nullable=False,
            server_default="30",
        ),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("last_triggered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint("daily_limit_minutes > 0", name="thresholds_limit_positive"),
        sa.UniqueConstraint("user_id", "category", name="uq_thresholds_user_category"),
    )
    op.create_index(
        "idx_thresholds_active",
        "thresholds",
        ["user_id"],
        postgresql_where=sa.text("enabled = TRUE"),
    )

    # weekly_reports
    op.create_table(
        "weekly_reports",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("week_start_date", sa.Date, nullable=False),
        sa.Column("total_minutes", sa.Integer, nullable=False),
        sa.Column("recovered_minutes", sa.Integer, nullable=False),
        sa.Column("recovered_won", sa.Integer, nullable=True),
        sa.Column("llm_card_text", sa.Text, nullable=False),
        sa.Column("llm_card_insight", sa.Text, nullable=True),
        sa.Column("llm_service_used", sa.String(20), nullable=True),
        sa.Column("any_channel_sent", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("user_id", "week_start_date", name="uq_weekly_reports_user_week"),
    )
    op.create_index(
        "idx_weekly_reports_user_week",
        "weekly_reports",
        ["user_id", sa.text("week_start_date DESC")],
    )

    # subscriptions (Google Play Billing V1, Toss V2)
    op.create_table(
        "subscriptions",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("source", sa.String(20), nullable=False, server_default="google_play"),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("gp_purchase_token", sa.String(500), nullable=True, unique=True),
        sa.Column("gp_order_id", sa.String(100), nullable=True),
        sa.Column("gp_product_id", sa.String(100), nullable=True),
        sa.Column("toss_payment_key", sa.String(255), nullable=True),
        sa.Column("toss_order_id", sa.String(100), nullable=True),
        sa.Column("amount_krw", sa.Integer, nullable=False),
        sa.Column("net_krw", sa.Integer, nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("trial_starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("promo_code", sa.String(50), nullable=True),
        sa.Column("discount_percent", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "source IN ('google_play', 'toss')", name="subs_source_check",
        ),
        sa.CheckConstraint(
            "kind IN ('one_time', 'monthly', 'yearly')", name="subs_kind_check",
        ),
        sa.CheckConstraint(
            "status IN ('active', 'in_trial', 'cancelled', 'expired', 'refunded')",
            name="subs_status_check",
        ),
    )
    op.create_index(
        "idx_subscriptions_user_active",
        "subscriptions",
        ["user_id"],
        postgresql_where=sa.text("status IN ('active', 'in_trial')"),
    )
    op.create_index(
        "idx_subscriptions_expires",
        "subscriptions",
        ["expires_at"],
        postgresql_where=sa.text("status = 'active'"),
    )
    op.create_index("idx_subscriptions_gp_token", "subscriptions", ["gp_purchase_token"])


def downgrade() -> None:
    op.drop_table("subscriptions")
    op.drop_table("weekly_reports")
    op.drop_table("thresholds")
    op.drop_table("fcm_tokens")
    op.drop_table("channel_subscriptions")
    op.drop_table("usage_event_dedupe")

    # drop partitions first
    for year, month in [(2026, m) for m in range(6, 13)]:
        op.execute(f"DROP TABLE IF EXISTS usage_events_y{year}m{month:02d}")
    op.execute("DROP TABLE IF EXISTS usage_events")

    op.drop_table("refresh_tokens")
    op.drop_table("users")
