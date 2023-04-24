from concurrent.futures import Future
from unittest.mock import AsyncMock, MagicMock, patch
import random
import uuid

from fastapi import HTTPException, status
import pytest
from sqlmodel import select, func

from phoenix.models.prime import Prime
from phoenix.models.task import Task, TaskResult, TaskStatus
from phoenix.services.primes import is_prime
from phoenix.services.tasks import task_for_number, task_result, process_task


@pytest.fixture(scope="session")
def future_with_true_as_result():
    fut = Future()
    fut.set_result(True)
    yield fut


@pytest.fixture(scope="session")
def future_with_false_as_result():
    fut = Future()
    fut.set_result(False)
    yield fut


@pytest.mark.asyncio
async def test_task_for_number(test_session):
    number = random.randint(0, 10000000000000)

    task = await task_for_number(number, test_session)

    assert task.number == number
    assert task.status == TaskStatus.New


@pytest.mark.asyncio
async def test_task_result(test_tasks, test_session):
    test_task = test_tasks[0]
    task = await task_result(test_task.id, test_session)

    assert test_task.id == task.id


@pytest.mark.asyncio
async def test_task_result_not_found(test_session):
    task_id = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        await task_result(task_id, test_session)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_process_task_new_prime_number(
    test_session, primes_testset, test_async_sessionmaker, future_with_true_as_result
):
    test_prime = random.choice(primes_testset)
    new_task = await task_for_number(test_prime, test_session)

    with patch("phoenix.services.tasks.executor_pool") as mock_executor_pool, patch(
        "phoenix.services.tasks.async_session"
    ) as mock_async_session:
        mock_executor = MagicMock()
        mock_executor.submit.return_value = future_with_true_as_result
        mock_executor_pool.return_value = mock_executor
        mock_async_session.return_value = test_async_sessionmaker()

        await process_task(new_task)
        await test_session.refresh(new_task)

        mock_executor_pool.assert_called_once()
        mock_executor.submit.assert_called_once_with(is_prime, test_prime)
        assert new_task.is_prime
        assert new_task.status == TaskStatus.Finished
        assert (
            await test_session.execute(
                select(func.count(Prime.id)).where(Prime.number == test_prime)
            )
        ).scalar() == 1


@pytest.mark.asyncio
async def test_process_task_precalculated_prime_number(
    test_session, test_primes, test_async_sessionmaker
):
    test_prime = random.choice(test_primes).number
    new_task = await task_for_number(test_prime, test_session)

    with patch("phoenix.services.tasks.executor_pool") as mock_executor_pool, patch(
        "phoenix.services.tasks.async_session"
    ) as mock_async_session:
        mock_executor = MagicMock()
        mock_async_session.return_value = test_async_sessionmaker()

        await process_task(new_task)
        await test_session.refresh(new_task)

        mock_executor_pool.assert_not_called()
        mock_executor.submit.assert_not_called()
        assert new_task.is_prime
        assert new_task.status == TaskStatus.Finished
        assert (
            await test_session.execute(
                select(func.count(Prime.id)).where(Prime.number == test_prime)
            )
        ).scalar() == 1


@pytest.mark.asyncio
async def test_process_task_not_prime_number(
    test_session, test_async_sessionmaker, future_with_false_as_result
):
    test_number = 4
    new_task = await task_for_number(test_number, test_session)

    with patch("phoenix.services.tasks.executor_pool") as mock_executor_pool, patch(
        "phoenix.services.tasks.async_session"
    ) as mock_async_session:
        mock_executor = MagicMock()
        mock_executor.submit.return_value = future_with_false_as_result
        mock_executor_pool.return_value = mock_executor
        mock_async_session.return_value = test_async_sessionmaker()

        await process_task(new_task)
        await test_session.refresh(new_task)

        mock_executor_pool.assert_called_once()
        mock_executor.submit.assert_called_once_with(is_prime, test_number)
        assert not new_task.is_prime
        assert new_task.status == TaskStatus.Finished
        assert (
            await test_session.execute(
                select(func.count(Prime.id)).where(Prime.number == test_number)
            )
        ).scalar() == 0
