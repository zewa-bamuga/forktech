import asyncio
import gzip
import lzma
from contextlib import contextmanager
from unittest.mock import AsyncMock, Mock, patch

import pytest
from a8t_tools.storage.local_storage import LocalStorageBackend
from celery import Celery
from freezegun import freeze_time

import app.domain
from app.fastapi import fastapi_app
from tests import __root_dir__, utils


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def frozen_time():
    with freeze_time() as ft:
        with patch("asyncio.sleep", new_callable=AsyncMock):
            yield ft


@pytest.fixture(scope="session")
def client(event_loop):
    yield utils.TestClientSessionExpire(fastapi_app)


@pytest.fixture(scope="session")
def container(client):
    client.application.extra["container"].wire(packages=[app.domain])
    yield client.application.extra["container"]


@pytest.fixture()
def container_singletone(container):
    with patch("app.containers.Container", new=lambda: container):
        yield container


@pytest.fixture()
def db_transaction():
    return fastapi_app.extra["container"].transaction()