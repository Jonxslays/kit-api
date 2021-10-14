import functools
import os
import random
import typing as t

from fastapi.exceptions import HTTPException

from kitapi import core


async def get_random_fact() -> core.models.Facts:
    """Gets the total number of facts in the database."""
    count = await core.models.Facts.all().count()
    data = (await core.models.Facts.all())[random.randint(0, count - 1)]

    if not data:
        raise core.DatabaseConnectionError("Failed to query the database.")

    return data


async def get_request_total() -> int:
    """Gets the total number of requests made to v1."""
    data = await core.models.Systems.get(version=1)

    if not data:
        raise core.DatabaseConnectionError("Failed to query the database.")

    return data.total_requests


@functools.lru_cache
def get_master_key() -> str:
    """Gets the V1 master key from the environment."""
    key: str | None = os.environ.get("V1_MASTER_KEY")

    if key is not None:
        return key

    raise core.MissingMasterKey("No API master key was found in the environment.")


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
        if not (query := await core.models.Systems.filter(version=1)):
            obj = await core.models.Systems.create(version=1)

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
        except core.DatabaseConnectionError:
            raise HTTPException(
                status_code=418,
                detail={
                    "error": "The server is refusing to be a coffee pot.",
                },
            )

        return result

    return predicate
