import abc


class Checker(abc.ABC):
    @abc.abstractmethod
    def check(self) -> None:
        pass
