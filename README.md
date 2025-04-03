# Модуль умной задержки

Объект SmartSleep оборачивает целевую функцию в "умный" объект через декоратор. Функционал позволяет сделать автоповтор функции с динамической задержкой между вызовами

## Example
```python
from random import randint

from smart_sleep import SmartSleep


@SmartSleep(secs=5, max_tries=3, alert_func=lambda: print("error"))
def function_that_cause_random_exception(arg):
    if randint(1, 4) == 1:
        raise Exception("Random exception occurred")
    else:
        return "Success: " + arg


result = function_that_cause_random_exception("test")
print(result)
```
## Install
- Скопировать `smart_sleep.py` в корень проекта
- Импортировать в другом файле `from smart_sleep import SmartSleep`
## Requirements
`python >= 3.7`
