"""backfill usage_events partitions for 2026-01 ~ 2026-05

001_initial created partitions starting at 2026-06, but the app may run /
ingest events during earlier months (current month = 2026-05, plus manual
backfill of recent days that can cross a month boundary). Without a matching
partition, INSERT fails with "no partition of relation found for row".

This adds 2026-01 ~ 2026-05 so the partition coverage is continuous from the
start of the launch year. Future months are handled by the monthly
create_next_partition cron (ARCHITECTURE §7).

Revision ID: 002
Revises: 001
"""

from collections.abc import Sequence

from alembic import op

revision: str = "002"
down_revision: str | Sequence[str] | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_MONTHS = [(2026, m) for m in range(1, 6)]  # 2026-01 ~ 2026-05


def upgrade() -> None:
    for year, month in _MONTHS:
        next_y, next_m = (year, month + 1) if month < 12 else (year + 1, 1)
        op.execute(
            f"""
            CREATE TABLE IF NOT EXISTS usage_events_y{year}m{month:02d}
            PARTITION OF usage_events
            FOR VALUES FROM ('{year}-{month:02d}-01')
                        TO ('{next_y}-{next_m:02d}-01')
            """,
        )


def downgrade() -> None:
    for year, month in _MONTHS:
        op.execute(f"DROP TABLE IF EXISTS usage_events_y{year}m{month:02d}")
