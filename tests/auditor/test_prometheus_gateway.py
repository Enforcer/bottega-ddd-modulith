from unittest import mock

from auditor import prometheus_gateway
from prometheus_client import Metric


def test_passes_metrics_as_gauges() -> None:
    metric = prometheus_gateway.PrometheusGateway.Metric(
        name="test_metric",
        description="test metric 123",
        value=123.0,
    )

    gateway = prometheus_gateway.PrometheusGateway(host_port="prometheus:9090")
    with mock.patch.object(
        prometheus_gateway, "push_to_gateway"
    ) as mock_push_to_gateway:
        gateway.push_metrics(job="test job", metrics=[metric])

    mock_push_to_gateway.assert_called_once()
    call = mock_push_to_gateway.mock_calls[0]
    assert call.kwargs["gateway"] == "prometheus:9090"
    assert call.kwargs["job"] == "test job"
    registry = call.kwargs["registry"]
    metrics_by_name = {metric.name: metric for metric in registry.collect()}
    assert _get_value_from_metrics(metrics_by_name["test_metric"]) == 123.0


def _get_value_from_metrics(metric: Metric) -> float:
    samples = metric.samples
    assert len(samples) == 1
    return samples[0].value
