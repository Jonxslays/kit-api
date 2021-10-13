import random
import typing as t

from fastapi import APIRouter, Header, HTTPException

from kitapi.v1 import utils
from kitapi.core.models import *

__all__: list[str] = ["FactRouter"]


FactRouter = APIRouter()


@FactRouter.get(
    "/fact",
    summary="Get random fact.",
    tags=["Facts"],
    responses={
        200: {"description": "A random fact."},
    }
)
@utils.handle_db_conn_exc
@utils.with_request_update
async def get_a_random_fact() -> Fact:
    """Gets a random fact."""
    id = random.randint(1, await utils.get_fact_total())
    obj = await Facts.get(id=id)
    obj.uses += 1
    await obj.save()
    return await Fact.from_tortoise_orm(obj)


@FactRouter.get(
    "/fact/{id}",
    summary="Get fact by ID.",
    tags=["Facts"],
    responses={
        200: {"description": "The requested fact."},
        404: {"description": "Not found."},
    },
)
@utils.with_request_update
async def get_a_fact_by_id(id: int) -> Fact:
    """Gets a fact by ID."""
    obj = await Facts.get(id=id)
    obj.uses += 1
    await obj.save()
    return await Fact.from_tortoise_orm(obj)


@FactRouter.patch(
    "/fact/{id}",
    summary="Update fact by ID.",
    tags=["Facts"],
    responses={
        200: {"description": "The updated fact."},
        400: {"description": "Bad request."},
        404: {"description": "Not found."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def update_a_fact(id: int, fact: FactIn, x_api_key: t.Any = Header(None)) -> Fact:
    """Updates a fact by ID."""
    obj = await Facts.get(id=id)
    f = fact.dict().get("fact")

    if not isinstance(f, str) or len(f) < 13:
        # I have arbitrarily chosen 13 characters as the minumum length fact...
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Bad request",
                "message": "Fact must be 13 chars in length and of type `str`.",
            }
        )

    obj.fact = f
    await obj.save()
    return await Fact.from_tortoise_orm(obj)


@FactRouter.delete(
    "/fact/{id}",
    summary="Delete a fact.",
    tags=["Facts"],
    status_code=200,
    responses={
        200: {"description": "The deleted fact."},
        403: {"description": "Forbidden."},
        404: {"description": "Not found."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def delete_a_fact(id: int, x_api_key: t.Any = Header(None)) -> Fact:
    """Deletes a fact from the database."""
    obj = removed = await Facts.get(id=id)
    await obj.delete()
    await obj.save()
    return await Fact.from_tortoise_orm(removed)


@FactRouter.post(
    "/fact",
    summary="Create a fact.",
    tags=["Facts"],
    status_code=201,
    responses={
        201: {"description": "The created fact."},
        403: {"description": "Forbidden."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def create_a_fact(fact: FactIn, x_api_key: t.Any = Header(None)) -> Fact:
    """Creates a new fact.
    * Requires the master api key.
    """
    obj = await Facts.create(**fact.dict())
    return await Fact.from_tortoise_orm(obj)


@FactRouter.get(
    "/system/requests",
    summary="Get total request count.",
    tags=["System"],
    responses={
        200: {"description": "The requested amount."},
    },
)
@utils.with_request_update
async def get_total_requests() -> int:
    """Fetches the total number of requests handled by v1 to date."""
    return await utils.get_request_total()
