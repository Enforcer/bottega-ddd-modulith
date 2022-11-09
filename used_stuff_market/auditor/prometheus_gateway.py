class PrometheusGateway:
    def __init__(self, host: str, port: int) -> None:
        self.host_port = f"{host}:{port}"
