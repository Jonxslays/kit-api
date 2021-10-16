import functools
import os
import random
import typing as t

from fastapi.exceptions import HTTPException

from kitapi.core import *


async def get_random_fact() -> models.Fact:
    """Gets the total number of facts in the database."""
    count = await models.Fact.all().count()
    data = (await models.Fact.all())[random.randint(0, count - 1)]

    if not data:
        raise DatabaseConnectionError("Failed to query the database.")

    return data


async def get_request_total() -> int:
    """Gets the total number of requests made to v1."""
    data = await models.System.get(version=1)

    if not data:
        raise DatabaseConnectionError("Failed to query the database.")

    return data.total_requests


@functools.lru_cache
def get_master_key() -> str:
    """Gets the V1 master key from the environment."""
    key: str | None = os.environ.get("V1_MASTER_KEY")

    if key is not None:
        return key

    raise MissingMasterKey("No API master key was found in the environment.")


def require_master_key(func: t.Any) -> t.Callable[..., t.Any]:
    """Decorates an endpoint to require the v1 master key."""

    @functools.wraps(func)
    async def predicate(x_api_key: str, *args: t.Any, **kwargs: t.Any) -> t.Any:
        if x_api_key != get_master_key():
            raise HTTPException(
                status_code=403, detail={"error": "Forbidden", "message": "Invalid API key."}
            )

        return await func(*args, **kwargs)

    return predicate


def with_request_update(func: t.Any) -> t.Callable[..., t.Any]:
    """Decorates endpoints to increment the total request count."""

    @functools.wraps(func)
    async def predicate(*args: t.Any, **kwargs: t.Any) -> t.Any:
        if not (query := await models.System.filter(version=1)):
            obj = await models.System.create(version=1)

        else:
            obj = query[0]
            obj.total_requests += 1

        await obj.save()
        return await func(*args, **kwargs)

    return predicate


def handle_db_conn_exc(func: t.Any) -> t.Callable[..., t.Any]:
    """Handles database connection errors."""

    @functools.wraps(func)
    async def predicate(*args: t.Any, **kwargs: t.Any) -> t.Any:
        try:
            result = await func(*args, **kwargs)
        except DatabaseConnectionError:
            raise HTTPException(
                status_code=418,
                detail={
                    "error": "The server is refusing to be a coffee pot.",
                },
            )

        return result

    return predicate
