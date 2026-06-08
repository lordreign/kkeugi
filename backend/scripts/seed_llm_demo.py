#!/usr/bin/env python3
"""실 LLM(Anthropic Haiku) 카드 생성 검증용 데이터 시드.

사용
    python3 scripts/seed_llm_demo.py [--email llmtest@kkeugi.kr] [--cleanup]

흐름
    1) dev_login 으로 토큰 발급 (개발 환경에서만 가능)
    2) 지난 7일 동안 매일 1개씩 usage_event 시드 — active filter 통과용
    3) /v1/usage/stats/week 로 시드 결과 확인
    4) (선택) --cleanup 으로 시드된 사용자·이벤트·리포트·구독 모두 제거

전제
    - 백엔드 실행 중: cd backend && make run
    - postgres 컨테이너 동작 중: make db-up
    - .env 의 ANTHROPIC_API_KEY 설정 (실 LLM 검증 위해)
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request as u
import uuid

BASE_URL = "http://localhost:8080"
DEFAULT_EMAIL = "llmtest@kkeugi.kr"
DEFAULT_NAME = "LLM Test"

# 7일치 시드 계획 — (days_ago, category, duration_seconds).
# 다양한 카테고리·시간대로 분산해 회고 카드의 인사이트(요일·카테고리 패턴)가
# 의미 있게 생성되도록 구성.
PLAN: list[tuple[int, str, int]] = [
    (0, "sns",     1800),  # 오늘 30분
    (1, "shorts",  2400),  # 어제 40분
    (2, "game",    3600),  # 60분
    (3, "webtoon", 1200),  # 20분
    (4, "sns",     2700),  # 45분
    (5, "shorts",  1500),  # 25분
    (6, "sns",     3000),  # 50분
]


def _post(path: str, body: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = u.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(body).encode(),
        headers=headers,
    )
    try:
        return json.loads(u.urlopen(req).read())
    except urllib.error.HTTPError as e:
        print(f"  ✗ {path} HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        raise


def _get(path: str, token: str) -> dict:
    req = u.Request(
        f"{BASE_URL}{path}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return json.loads(u.urlopen(req).read())


def dev_login(email: str, name: str) -> str:
    print(f"▸ dev_login {email}")
    resp = _post("/v1/auth/dev/login", {"email": email, "name": name})
    tok = resp["access_token"]
    print(f"  토큰 prefix: {tok[:24]}...")
    return tok


def seed_usage(token: str) -> None:
    print(f"▸ 지난 7일 usage_events 시드 ({len(PLAN)}건)")
    now = datetime.datetime.now(datetime.timezone.utc)
    events = []
    for d, cat, sec in PLAN:
        ts = (now - datetime.timedelta(days=d, hours=14)).replace(microsecond=0).isoformat()
        events.append({
            "client_event_id": str(uuid.uuid4()),
            "package_name": "com.instagram.android",
            "category": cat,
            "duration_seconds": sec,
            "occurred_at": ts,
            "source": "usagestats",
        })
    resp = _post("/v1/usage/batch", {"events": events}, token)
    print(f"  ✓ accepted: {len(resp['accepted'])} / duplicate: {len(resp['duplicate'])}")


def print_week_stats(token: str) -> None:
    stats = _get("/v1/usage/stats/week", token)
    print()
    print(f"▸ stats/week — 총 {stats['total_minutes']}분")
    for c in stats["by_category"]:
        print(f"    {c['category']:<8} {c['minutes']:>3}분")
    print("  일별:")
    for d in stats["by_day"]:
        bar = "█" * max(0, d["total_minutes"] // 5)
        print(f"    {d['date']} {d['total_minutes']:>3}분  {bar}")


def cleanup(email: str) -> None:
    import subprocess
    print(f"▸ cleanup {email}")
    sql = f"""
DELETE FROM weekly_reports WHERE user_id IN (SELECT id FROM users WHERE email='{email}');
DELETE FROM subscriptions  WHERE user_id IN (SELECT id FROM users WHERE email='{email}');
DELETE FROM usage_events   WHERE user_id IN (SELECT id FROM users WHERE email='{email}');
DELETE FROM usage_event_dedupe WHERE user_id IN (SELECT id FROM users WHERE email='{email}');
DELETE FROM users WHERE email='{email}';
"""
    r = subprocess.run(
        ["docker", "exec", "kkeugi-pg", "psql", "-U", "postgres", "-d", "kkeugi", "-c", sql],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"  ✗ {r.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ 정리 완료\n{r.stdout}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--email", default=DEFAULT_EMAIL, help="dev 사용자 이메일")
    p.add_argument("--name", default=DEFAULT_NAME, help="dev 사용자 이름")
    p.add_argument("--cleanup", action="store_true", help="시드된 사용자/데이터 모두 제거 후 종료")
    args = p.parse_args()

    if args.cleanup:
        cleanup(args.email)
        return

    token = dev_login(args.email, args.name)
    seed_usage(token)
    print_week_stats(token)

    print()
    print("=" * 60)
    print("다음 단계 (STEP 5) — 실 LLM 트리거")
    print("=" * 60)
    print("  time curl -s -X POST http://localhost:8080/v1/reports/dev/run_weekly | python3 -m json.tool")
    print()
    print("성공 시 응답: {\"generated\": 1}")
    print("응답 시간 1~5초면 Anthropic 실 호출 (Fake 는 ms 단위).")


if __name__ == "__main__":
    main()
