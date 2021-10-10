import random
import typing as t

from fastapi import APIRouter, Header

from kitapi.v1 import utils
from kitapi.core.models import *

__all__: list[str] = ["FactRouter"]


FactRouter = APIRouter()


@FactRouter.get(
    "/fact",
    summary="Get random fact.",
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
    responses={
        200: {"description": "The requested fact."},
        404: {"description": "Not Found."},
    },
)
@utils.with_request_update
async def get_a_fact_by_id(id: int) -> Fact:
    """Gets a fact by ID."""
    obj = await Facts.get(id=id)
    obj.uses += 1
    await obj.save()
    return await Fact.from_tortoise_orm(obj)


@FactRouter.post(
    "/fact",
    summary="Create a fact.",
    status_code=201,
    responses={
        201: {"description": "The created fact."},
        403: {"description": "Forbidden."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def create_a_fact(
    fact: FactIn,
    x_api_key: t.Any = Header(None),
) -> Fact:
    """Creates a new fact.
    * Requires the master api key.
    """
    obj = await Facts.create(**fact.dict())
    return await Fact.from_tortoise_orm(obj)
