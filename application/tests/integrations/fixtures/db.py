import asyncio

import pytest
import pytest_asyncio

from database import async_engine, async_session
from users.models import Users


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Users.metadata.drop_all)
        await conn.run_sync(Users.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Users.metadata.drop_all)
