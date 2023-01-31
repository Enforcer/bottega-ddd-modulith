import pytest
from fastapi.testclient import TestClient

from tests.acceptance.app_client import AppClient
from tests.acceptance.features import (
    Buying,
    Catalog,
    Items,
    Likes,
    Negotiations,
    Payments,
    Users,
)


@pytest.fixture()
def app_client(client: TestClient) -> AppClient:
    return AppClient(client)


@pytest.fixture()
def users(app_client: AppClient) -> Users:
    return Users(app_client)


@pytest.fixture()
def items(app_client: AppClient) -> Items:
    return Items(app_client)


@pytest.fixture()
def likes(app_client: AppClient) -> Likes:
    return Likes(app_client)


@pytest.fixture()
def buying(app_client: AppClient) -> Buying:
    return Buying(app_client)


@pytest.fixture()
def payments(app_client: AppClient) -> Payments:
    return Payments(app_client)


@pytest.fixture()
def catalog(app_client: AppClient) -> Catalog:
    return Catalog(app_client)


@pytest.fixture()
def negotiations(app_client: AppClient) -> Negotiations:
    return Negotiations(app_client)
