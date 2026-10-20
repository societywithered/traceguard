import functools
import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class RunRecord:
    function: str
    duration_ms: float
    succeeded: bool
    error: str | None = None


class TraceGuard:
    def __init__(self):
        self.records: list[RunRecord] = []

    def watch(self, func: F) -> F:
        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                self.records.append(RunRecord(
                    func.__qualname__,
                    (time.perf_counter() - start) * 1000,
                    False,
                    f"{type(exc).__name__}: {exc}",
                ))
                raise

            self.records.append(RunRecord(
                func.__qualname__,
                (time.perf_counter() - start) * 1000,
                True,
            ))
            return result

        return cast(F, wrapped)

    def report(self) -> str:
        return json.dumps([asdict(record) for record in self.records], indent=2)

    def clear(self) -> None:
        self.records.clear()