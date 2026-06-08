"""error_notifier 단위 테스트 — cooldown·fingerprint·format 순수 검증."""
from datetime import UTC, datetime, timedelta

from app.observability.error_notifier import (
    CooldownState,
    format_message,
    make_fingerprint,
    should_notify,
)


def test_fingerprint_same_for_same_input():
    e1 = ValueError("x")
    e2 = ValueError("x")
    assert make_fingerprint("/a", e1) == make_fingerprint("/a", e2)


def test_fingerprint_differs_by_path():
    e = ValueError("x")
    assert make_fingerprint("/a", e) != make_fingerprint("/b", e)


def test_fingerprint_differs_by_exception_class():
    assert make_fingerprint("/a", ValueError("x")) != make_fingerprint("/a", KeyError("x"))


def test_fingerprint_differs_by_message():
    assert make_fingerprint("/a", ValueError("x")) != make_fingerprint("/a", ValueError("y"))


def test_should_notify_first_call_returns_true():
    st = CooldownState()
    now = datetime.now(UTC)
    assert should_notify(st, "fp1", now, timedelta(seconds=300)) is True
    assert st.last_sent["fp1"] == now


def test_should_notify_within_cooldown_returns_false():
    st = CooldownState()
    t0 = datetime.now(UTC)
    should_notify(st, "fp", t0, timedelta(seconds=300))
    # 4분 후 — cooldown 안
    t1 = t0 + timedelta(seconds=240)
    assert should_notify(st, "fp", t1, timedelta(seconds=300)) is False
    assert st.skipped_count["fp"] == 1


def test_should_notify_after_cooldown_returns_true():
    st = CooldownState()
    t0 = datetime.now(UTC)
    should_notify(st, "fp", t0, timedelta(seconds=300))
    # 6분 후 — cooldown 지남
    t1 = t0 + timedelta(seconds=360)
    assert should_notify(st, "fp", t1, timedelta(seconds=300)) is True
    assert st.skipped_count["fp"] == 0  # reset


def test_should_notify_different_fingerprints_independent():
    st = CooldownState()
    now = datetime.now(UTC)
    assert should_notify(st, "a", now, timedelta(seconds=300)) is True
    assert should_notify(st, "b", now, timedelta(seconds=300)) is True


def test_format_message_includes_path_and_exception():
    try:
        raise ValueError("boom")
    except ValueError as e:
        msg = format_message(path="POST /v1/x", exc=e)
    assert "POST /v1/x" in msg
    assert "ValueError" in msg
    assert "boom" in msg


def test_format_message_includes_user_context():
    msg = format_message(
        path="GET /v1/y",
        exc=KeyError("k"),
        user_email="u@test.com",
        user_id="abcdef12-3456-...",
    )
    assert "u@test.com" in msg
    assert "abcdef12" in msg


def test_format_message_truncates_long_trace():
    """매우 긴 trace 라도 4096자 안전."""
    try:
        raise RuntimeError("x" * 5000)
    except RuntimeError as e:
        msg = format_message(path="/p", exc=e)
    assert len(msg) < 4096


def test_format_message_includes_skipped_count():
    msg = format_message(path="/p", exc=ValueError("v"), skipped_since=42)
    assert "42" in msg
