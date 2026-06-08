#!/usr/bin/env python3
"""특정 사용자의 weekly_report 가 어떤 입력으로 만들어졌는지 역추적.

사용
    python3 scripts/show_llm_context.py [--email llmtest@kkeugi.kr]

출력
    1) 저장된 weekly_reports 행 (LLM 결과)
    2) 이번 주 raw usage_events (LLM 입력의 원천)
    3) compute_week_stats 가 재현한 5개 CardContext 필드 (LLM 에 실제 전달된 값)
    4) AnthropicLLM.generate() 가 실제로 보낸 prompt 재구성
    5) 결정론적 insight 후처리 결과

추적 흐름
    usage_events (행 단위 raw)
        ↓ compute_week_stats (집계, service.py)
    CardContext 5필드
        ↓ AnthropicLLM.generate() (prompt 조립, llm.py)
    Anthropic Haiku API
        ↓
    llm_card_text + llm_card_insight (weekly_reports 저장)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# 백엔드 코드 그대로 재사용 (집계 로직 = production 흐름과 동일)
sys.path.insert(0, ".")
from app.config import get_settings  # noqa: E402
from app.reports.models import WeeklyReport  # noqa: E402
from app.reports.service import _utc_range, compute_week_stats, week_start_for  # noqa: E402
from app.usage.models import UsageEvent  # noqa: E402
from app.users.models import User  # noqa: E402


async def show(email: str) -> None:
    s = get_settings()
    engine = create_async_engine(s.database_url, future=True)
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as db:
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()
        if user is None:
            print(f"✗ 사용자 {email} 없음")
            return
        print(f"▸ 사용자: {user.email}  id={user.id}  tz={user.timezone}")
        print(f"  hourly_value: {user.hourly_value or '미설정 (recovered_won = null)'}")

        tz = ZoneInfo(user.timezone)
        today = datetime.now(tz).date()
        ws = week_start_for(today)
        last_ws = ws - timedelta(days=7)
        print(f"  이번 주 시작 (월): {ws}  /  지난 주 시작: {last_ws}")

        # 1) 저장된 weekly_reports
        print()
        print("=" * 70)
        print("1. 저장된 weekly_reports 행 (LLM 결과)")
        print("=" * 70)
        rep = (
            await db.execute(
                select(WeeklyReport).where(
                    WeeklyReport.user_id == user.id,
                    WeeklyReport.week_start_date == ws,
                ),
            )
        ).scalar_one_or_none()
        if rep is None:
            print(f"  (이번 주 {ws} 리포트 없음 — dev/run_weekly 먼저 실행)")
        else:
            print(f"  llm_service_used  : {rep.llm_service_used}")
            print(f"  total_minutes     : {rep.total_minutes}")
            print(f"  recovered_minutes : {rep.recovered_minutes}")
            print(f"  recovered_won     : {rep.recovered_won}")
            print(f"  any_channel_sent  : {rep.any_channel_sent}")
            print(f"  card_text         : {rep.llm_card_text}")
            print(f"  card_insight      : {rep.llm_card_insight}")

        # 2) raw usage_events 이번 주
        print()
        print("=" * 70)
        print("2. 이번 주 raw usage_events (LLM 입력의 원천)")
        print("=" * 70)
        start_utc, end_utc = _utc_range(ws, tz)
        rows = (
            await db.execute(
                select(UsageEvent)
                .where(
                    UsageEvent.user_id == user.id,
                    UsageEvent.occurred_at >= start_utc,
                    UsageEvent.occurred_at < end_utc,
                )
                .order_by(UsageEvent.occurred_at),
            )
        ).scalars().all()
        if not rows:
            print(f"  이번 주 ({ws}~{ws + timedelta(days=7)}) raw 이벤트 0건")
        else:
            print(f"  {len(rows)}건  (UTC {start_utc} ~ {end_utc})")
            for r in rows:
                local = r.occurred_at.astimezone(tz)
                mins = r.duration_seconds // 60
                print(
                    f"    {local.strftime('%a %m-%d %H:%M')} "
                    f"{r.category:<8} {r.duration_seconds:>5}초 "
                    f"({mins:>3}분)  {r.package_name}",
                )

        # 지난 주 집계 — recovered_minutes 계산 base
        print()
        print("   [지난 주 카테고리 합 — recovered_minutes 계산 base]")
        last_start_utc, last_end_utc = _utc_range(last_ws, tz)
        last_rows = (
            await db.execute(
                select(UsageEvent.category, func.sum(UsageEvent.duration_seconds))
                .where(
                    UsageEvent.user_id == user.id,
                    UsageEvent.occurred_at >= last_start_utc,
                    UsageEvent.occurred_at < last_end_utc,
                )
                .group_by(UsageEvent.category),
            )
        ).all()
        last_by_cat = {cat: round((secs or 0) / 60) for cat, secs in last_rows}
        last_total = sum(last_by_cat.values())
        print(f"   지난주 total: {last_total}분  /  by_category: {last_by_cat}")

        # 3) compute_week_stats 재현 = LLM 입력 5필드
        print()
        print("=" * 70)
        print("3. compute_week_stats 재현 → CardContext (LLM 에 실제 전달된 값)")
        print("=" * 70)
        ws_this = await compute_week_stats(db, user.id, ws, tz)
        recovered_min = last_total - ws_this.total_minutes
        recovered_won = (
            round(recovered_min * user.hourly_value / 60)
            if user.hourly_value else None
        )
        print(f"  total_minutes      : {ws_this.total_minutes}")
        print(f"  recovered_minutes  : {recovered_min}   ← 지난주 {last_total} − 이번주 {ws_this.total_minutes}")
        print(f"  recovered_won      : {recovered_won}")
        print(f"  top_category_label : {ws_this.top_category!r}")
        print(f"  peak_label         : {ws_this.peak_label!r}")
        print(f"  by_category (이번주): {ws_this.by_category}")

        # 4) AnthropicLLM.generate() prompt 재구성 (llm.py 와 1:1)
        print()
        print("=" * 70)
        print("4. AnthropicLLM.generate() 가 Haiku 4.5 에 보낸 prompt 재구성")
        print("=" * 70)
        prompt = (
            f"이번 주 흩어진 시간 {ws_this.total_minutes}분, "
            f"지난주 대비 {recovered_min}분 "
            f"({'감소' if recovered_min >= 0 else '증가'}), "
            f"가장 많은 카테고리 {ws_this.top_category or '없음'}, "
            f"가장 흩어진 시간대 {ws_this.peak_label or '없음'}. "
            "이 사실로 회고 카드 본문(2~3문장)을 써줘."
        )
        print('  system : "거울 같은 친구" 톤  (llm.py _SYSTEM 상수)')
        print(f"  prompt :\n    {prompt}")
        print(f"  model  : claude-haiku-4-5-20251001  (max_tokens=300)")

        # 5) insight 결정론 후처리
        print()
        print("=" * 70)
        print("5. insight 후처리 (LLM 이 만드는 게 아님 — 코드가 결정론적 생성)")
        print("=" * 70)
        if ws_this.peak_label:
            insight = f"{ws_this.peak_label}에 가장 많이 흩어졌어요."
            print(f"  peak_label 있음 → insight = {insight!r}")
        else:
            print("  peak_label 없음 → insight = None")
            print("  (이번 주 데이터 0 또는 모든 요일·시간대 균등 분포 시 발생)")

    await engine.dispose()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--email", default="llmtest@kkeugi.kr")
    args = p.parse_args()
    asyncio.run(show(args.email))


if __name__ == "__main__":
    main()
