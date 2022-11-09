from dataclasses import dataclass

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


class PrometheusGateway:
    @dataclass(frozen=True)
    class Metric:
        name: str
        description: str
        value: float

    def __init__(self, host_port: str) -> None:
        self._host_port = host_port

    def push_metrics(self, job: str, metrics: list[Metric]) -> None:
        registry = CollectorRegistry()
        for metric in metrics:
            gauge = Gauge(metric.name, metric.description, registry=registry)
            gauge.set(metric.value)

        push_to_gateway(gateway=self._host_port, job=job, registry=registry)
