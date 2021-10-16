import typing as t

from fastapi import APIRouter, Header, HTTPException

from kitapi.core import models, schemas
from kitapi.v1 import utils

__all__: list[str] = ["FactRouter"]


FactRouter = APIRouter()


@FactRouter.get(
    "/fact",
    summary="Get a random fact.",
    tags=["Facts"],
    responses={
        200: {
            "description": "A random fact.",
            "model": schemas.Fact,
        },
    },
)
@utils.handle_db_conn_exc
@utils.with_request_update
async def get_a_random_fact() -> schemas.Fact:
    """Gets a random fact, you feelin lucky?"""
    obj = await utils.get_random_fact()
    obj.uses += 1
    await obj.save()
    return schemas.Fact.from_orm(obj)


@FactRouter.get(
    "/fact/{id}",
    summary="Get a fact.",
    tags=["Facts"],
    responses={
        200: {
            "description": "The requested fact.",
            "model": schemas.Fact,
        },
        404: {"description": "Not found."},
    },
)
@utils.with_request_update
async def get_a_fact_by_id(id: int) -> schemas.Fact:
    """Gets a fact by it's ID."""
    obj = await models.Fact.get(id=id)
    obj.uses += 1
    await obj.save()
    return schemas.Fact.from_orm(obj)


@FactRouter.patch(
    "/fact/{id}",
    summary="Update a fact.",
    tags=["Facts"],
    responses={
        200: {
            "description": "The updated fact.",
            "model": schemas.Fact,
        },
        400: {"description": "Bad request."},
        404: {"description": "Not found."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def update_a_fact(id: int, fact: schemas.FactIn, x_api_key: t.Any = Header(None)) -> schemas.Fact:
    """Updates a fact by it's ID.
    * Requires the master api key.
    """
    obj = await models.Fact.get(id=id)
    f = fact.dict().get("fact")

    if not isinstance(f, str) or len(f) < 13:
        # I have arbitrarily chosen 13 characters as the minumum length fact...
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Bad request",
                "message": "Fact must be 13 chars in length and of type `str`.",
            },
        )

    obj.fact = f
    await obj.save()
    return schemas.Fact.from_orm(obj)


@FactRouter.delete(
    "/fact/{id}",
    summary="Delete a fact.",
    tags=["Facts"],
    responses={
        200: {
            "description": "The deleted fact.",
            "model": schemas.Fact,
        },
        403: {"description": "Forbidden."},
        404: {"description": "Not found."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def delete_a_fact(id: int, x_api_key: t.Any = Header(None)) -> schemas.Fact:
    """Deletes a fact by it's ID.
    * Requires the master api key.
    """
    obj = removed = await models.Fact.get(id=id)
    await obj.delete()
    await obj.save()
    return schemas.Fact.from_orm(removed)


@FactRouter.post(
    "/fact/create",
    summary="Create a fact.",
    tags=["Facts"],
    status_code=201,
    responses={
        201: {
            "description": "The created fact.",
            "model": schemas.Fact,
        },
        403: {"description": "Forbidden."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def create_a_fact(fact: schemas.FactIn, x_api_key: t.Any = Header(None)) -> schemas.Fact:
    """Creates a new fact.
    * Requires the master api key.
    """
    obj = await models.Fact.create(**fact.dict())
    return schemas.Fact.from_orm(obj)


@FactRouter.post(
    "/fact/create/bulk",
    summary="Bulk create facts.",
    tags=["Facts"],
    status_code=201,
    responses={
        201: {
            "description": "The created facts.",
            "model": schemas.BulkFact,
        },
        400: {"description": "Bad request."},
        403: {"description": "Forbidden."},
    },
)
@utils.require_master_key
@utils.with_request_update
async def bulk_create_a_fact(
    facts: schemas.BulkFactIn,
    x_api_key: t.Any = Header(None)
) -> schemas.BulkFact:
    """Bulk creates new facts.

    ex: { 'facts': [
            { 'fact': 'Cats are awesome.'},
            { 'fact': 'Cats are cute.'}
        ]
    }

    * Requires the master api key.
    """

    results: list[schemas.Fact] = []

    for fact in facts.facts:
        obj = await models.Fact.create(**fact.dict())
        results.append(schemas.Fact.from_orm(obj))

    return schemas.BulkFact(facts=results)


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
