import json

import pytest

from traceguard import TraceGuard


def test_success():
    trace = TraceGuard()

    @trace.watch
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert trace.records[0].succeeded


def test_error():
    trace = TraceGuard()

    @trace.watch
    def fail():
        raise ValueError("bad input")

    with pytest.raises(ValueError):
        fail()

    assert not trace.records[0].succeeded
    assert trace.records[0].error == "ValueError: bad input"


def test_report_and_clear():
    trace = TraceGuard()

    @trace.watch
    def work():
        return "done"

    work()
    assert json.loads(trace.report())[0]["succeeded"]
    trace.clear()
    assert trace.records == []