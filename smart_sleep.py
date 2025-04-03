from dataclasses import dataclass
from time import sleep
from typing import Any, Callable, Optional


class MaxTries(Exception):
    """Ошибка максимального количества попыток

    Args:
        Exception (MaxTries): Достигнуто максимальное количество попыток
    """

    pass


@dataclass
class Answer:
    """Тип данных для хранения результата выполнения функции и ошибки"""

    result: Optional[Any] = None
    exception: Optional[Exception] = None


def try_exception() -> Callable[[Callable], Callable[[], Answer]]:
    """Оборачивает функцию в try-except конструкцию

    Returns:
        Callable[[Callable], Callable[[], Answer]]: Обёрнутая функция
    """

    def wrap(function: Callable) -> Callable[[], Answer]:
        def execute() -> Answer:
            try:
                result: Any = function()
                return Answer(result=result)
            except Exception as e:
                return Answer(exception=e)

        return execute

    return wrap


class SmartSleep:
    def __init__(
        self, secs: int = 60, max_tries: int = 0, alert_func: Optional[Callable] = None
    ):
        """Оборачивает функцию в "умную задержку"

        Args:
            secs (int, optional): Начальные секунды задержки. Defaults to 60.
            max_tries (int, optional): Максимальное количество попыток. Defaults to 0.
            alert_func (Optional[Callable], optional): Future. Defaults to None.
        """
        self.secs = secs
        self.max_tries = max_tries
        self.alert_func = alert_func

    def __call__(self, func: Callable) -> Callable:
        """Отработка вызова функции

        Args:
            func (Callable): Целевая функция

        Returns:
            Callable: Функция обёрнутая в "умную задержку"
        """

        def wrapped_function(*args, **kwargs) -> Any:
            wrapped_func: Callable[[], Answer] = try_exception()(
                lambda: func(*args, **kwargs)
            )
            return self._iter_sleep(wrapped_func, self.secs, self.max_tries, 1)

        return wrapped_function

    def _iter_sleep(
        self,
        wrapped_func: Callable[[], Answer],
        secs: int,
        max_tries: int,
        try_i: int,
    ) -> Any:
        """Вызов итерации задержки

        Args:
            wrapped_func (Callable[[], Answer]): Обёрнутая функция
            secs (int): Начальные секунды задержки
            max_tries (int): Максимальное количество попыток
            try_i (int): Номер попытки

        Raises:
            MaxTries: Достигнуто максимальное количество попыток

        Returns:
            Any: Результат выполнения функции (если успешен)
        """
        if max_tries > 0 and try_i > max_tries:
            raise MaxTries("Достигнуто максимальное количество попыток")

        answer: Answer = wrapped_func()

        if answer.result is not None:
            return answer.result
        elif answer.exception:
            print(answer.exception)

        if self.alert_func:
            self.alert_func(...)

        sleep_secs: int = secs * try_i
        sleep(sleep_secs)
        try_i += 1
        return self._iter_sleep(wrapped_func, secs, max_tries, try_i)
