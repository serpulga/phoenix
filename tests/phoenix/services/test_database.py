import random
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import ProgrammingError
from sqlmodel import func, select, SQLModel

from phoenix.models.prime import Prime
from phoenix.models.task import Task
from phoenix.services.database import engine, db_session, create_all


@pytest.mark.asyncio
async def test_create_all():
    with patch("phoenix.services.database.engine") as mock_engine:
        mock_conn = AsyncMock()
        mock_engine.begin.return_value.__aenter__.return_value = mock_conn

        await create_all()

        mock_conn.run_sync.assert_awaited_once_with(SQLModel.metadata.create_all)


@pytest.mark.asyncio
async def test_db_session():
    async for session in db_session():
        await create_all()
        # Asserts got a usable session object.
        test_model = random.choice([Prime, Task])
        assert (await session.execute(select(func.count(test_model.id)))).scalar() >= 0
