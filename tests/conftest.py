import asyncio
import pathlib

from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import delete, SQLModel

from main import app
from phoenix.models.task import Task, TaskStatus
from phoenix.models.prime import Prime
from phoenix.services.database import db_session
import settings


# Allows session-scoped fixtures that are async.
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_connection_url():
    yield settings.DATABASE_URL


@pytest.fixture(scope="session")
def engine(db_connection_url):
    engine = create_async_engine(db_connection_url)
    yield engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def test_async_sessionmaker(engine):
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest_asyncio.fixture(scope="function")
async def test_session(test_async_sessionmaker):
    async with test_async_sessionmaker() as session:
        await session.execute(delete(Prime))
        await session.execute(delete(Task))
        await session.commit()

        yield session


@pytest.fixture(scope="function", autouse=True)
def override_db_session_dependency(db_connection_url):
    async def _db_session():
        # Needs to create a new engine so that the
        # even loop associated is from FastAPI runtime.
        engine = create_async_engine(db_connection_url)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            yield session

    app.dependency_overrides[db_session] = _db_session

    yield


@pytest.fixture(scope="session")
def testdir():
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def testdir():
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def testset_dir(testdir):
    return testdir / pathlib.Path("primes_lower_1000.txt")


@pytest.fixture(scope="session")
def big_prime_number():
    return 40000967


@pytest.fixture(scope="session")
def big_non_prime_number():
    return 40000969


@pytest.fixture(scope="session")
def primes_testset(testset_dir):
    with open(testset_dir, "r") as testset:
        return [int(d) for d in testset.read().split(",")]


@pytest.fixture(scope="function")
def test_client():
    client = TestClient(app)
    yield client
    client.cookies.clear()


@pytest_asyncio.fixture(scope="function")
async def test_tasks(test_session):
    t = []
    for i in range(10):
        task = Task(number=i, status=TaskStatus.New)
        test_session.add(task)
        t.append(task)

    await test_session.commit()
    yield t


@pytest_asyncio.fixture(scope="function")
async def test_primes(test_session, primes_testset):
    p = []
    for number in primes_testset[:10]:
        prime = Prime(number=number)
        test_session.add(prime)
        p.append(prime)

    await test_session.commit()
    yield p
