import abc


class Checker(abc.ABC):
    def __init__(self, prometheus_host_port: str) -> None:
        self.prometheus_host_port = prometheus_host_port

    @abc.abstractmethod
    def check(self) -> None:
        pass
