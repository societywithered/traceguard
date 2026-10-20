# TraceGuard

Records function run times and errors.

## Install

```bash
pip install -e ".[dev]"# traceguard


#Use                               
          from traceguard import TraceGuard

trace = TraceGuard()

@trace.watch
def add(a, b):
    return a + b

print(add(2, 3))
print(trace.report())