import random
import typing

from fastapi import Response, Header, HTTPException, APIRouter

from kitapi.v1 import utils

__all__: list[str] = ["FactRouter"]


facts: list[str] = ["Cats are amazing.", "I wish I was a cat."]


FactRouter = APIRouter()


@FactRouter.get("/fact", status_code=200, response_description="A random fact.")
async def get_kit_fact(response: Response) -> dict[str, str]:
    """Returns a fact about a kit."""

    return {"fact": facts[random.randint(0, len(facts) - 1)]}


@FactRouter.post(
    "/fact/{fact}",
    status_code=201,
    responses={
        201: {"description": "The created fact."},
        403: {"description": "When an invalid api key is passed."}
    }
)
async def create_kit_fact(
    response: Response,
    fact: str,
    x_api_key: typing.Optional[str] = Header(None),
) -> dict[str, str]:
    if x_api_key == utils.get_master_key():
        facts.append(fact)
        return {"fact": fact}

    raise HTTPException(
        status_code=403,
        detail={
            "Error": 403,
            "Message": "Invalid API key."
        }
    )
