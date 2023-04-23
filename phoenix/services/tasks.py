import asyncio
from datetime import datetime
import time
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.logger import logger
from sqlmodel import select, Session, update

from phoenix.models.prime import Prime
from phoenix.models.task import Task, TaskStatus
from phoenix.services.database import db_session, async_session
from phoenix.services.parallel import executor_pool
from phoenix.services.primes import is_prime


async def task_for_number(
    number: int,
    session: Session = Depends(db_session),
) -> Task:
    task = Task(number=number, status=TaskStatus.New)
    session.add(task)
    await session.commit()

    return task


async def process_task(task: Task):
    async with async_session() as session:
        async with session.begin():
            calculated = (
                await session.execute(select(Prime).where(Prime.number == task.number))
            ).scalar()
            if calculated:
                logger.info("Found pre-calculated number=%s", task.number)
                is_prime_number = True
            else:
                logger.info("Calculating new for number=%s", task.number)
                el = asyncio.get_event_loop()
                t0 = time.time()
                is_prime_number = await el.run_in_executor(
                    executor_pool(), is_prime, task.number
                )
                logger.info(
                    "Calcuated number=%s is_prime=%s took=%.2f",
                    task.number,
                    is_prime_number,
                    time.time() - t0,
                )
                prime = Prime(number=task.number)
                session.add(prime)

            await session.execute(
                update(Task)
                .values(
                    is_prime=is_prime_number,
                    finished_at=datetime.utcnow(),
                    status=TaskStatus.Finished,
                )
                .where(Task.id == task.id)
            )
            await session.commit()


async def task_result(
    task_id: uuid.UUID,
    session: Session = Depends(db_session),
) -> Task:
    task = (await session.execute(select(Task).where(Task.id == task_id))).scalar()
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return task
