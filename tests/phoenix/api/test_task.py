import random
from unittest.mock import patch
import uuid

from fastapi import status
import pytest


class TestTaskAPI:
    API_BASE_URL = "/api/tasks"

    @pytest.mark.asyncio
    async def test_get_task(self, test_client, test_tasks):
        task = random.choice(test_tasks)
        response = test_client.get(f"{type(self).API_BASE_URL}/{str(task.id)}")
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response_json
        assert "number" in response_json
        assert "status" in response_json
        assert "is_prime" in response_json
        assert "finished_at" in response_json
        assert response_json["id"] == str(task.id)
        assert response_json["number"] == task.number
        assert response_json["status"] == task.status.value
        assert response_json["finished_at"] == task.finished_at

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, test_client, test_tasks):
        response = test_client.get(f"{type(self).API_BASE_URL}/{str(uuid.uuid4())}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
