import random
from unittest.mock import patch

from fastapi import status
import pytest
from sqlmodel import select

from phoenix.models.task import Task, TaskStatus


class TestPrimeAPI:
    API_BASE_URL = "/api/primes"

    @pytest.mark.asyncio
    @patch("phoenix.api.primes.process_task")
    async def test_is_prime(self, mock_process_task, test_session, test_client):
        test_number = random.randint(0, 1000000000)
        response = test_client.get(f"{type(self).API_BASE_URL}/{test_number}")
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response_json
        assert "number" in response_json
        assert "status" in response_json
        assert response_json["number"] == test_number
        assert response_json["status"] == TaskStatus.New.value
        assert (
            task := (
                await test_session.execute(
                    select(Task).where(
                        Task.id == response_json["id"],
                        Task.number == test_number,
                    )
                )
            ).scalar()
        )
        mock_process_task.assert_called_once()
        assert mock_process_task.call_args[0][0].id == task.id
