from concurrent.futures import ProcessPoolExecutor
from unittest.mock import patch

from fastapi import status
import pytest

from main import app, initialize_db, lifespan


def test_root(test_client):
    assert test_client.get("/").status_code == status.HTTP_200_OK


def test_lifespan():
    app.state.executor_pool = None
    next(lifespan(app))
    executor_after = getattr(app.state, "executor_pool", None)

    assert type(executor_after) == ProcessPoolExecutor


@pytest.mark.asyncio
@patch("main.create_all")
async def test_initizalize_db(mock_create_all):
    await initialize_db()

    mock_create_all.assert_awaited_once_with()
