# Модуль умной задержки

Объект SmartSleep оборачивает целевую функцию в "умный" декоратор с автоповтором и динамической задержкой между вызовами

## Example
```python
from random import randint

from .smart_sleep import SmartSleep


@SmartSleep(secs=5, max_tries=3)
def function_that_cause_random_exception(arg):
    if randint(1, 4) == 1:
        raise Exception("Random exception occurred")
    else:
        return "Success: " + arg


result = function_that_cause_random_exception("test")
print(result)
```
## Requirements
`python >= 3.7`
