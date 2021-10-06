import typing

import fastapi as fast

__all__:typing.List[str] = ["FactRouter",]


FactRouter = fast.APIRouter()


@FactRouter.get("/fact")
async def get_a_fact(response: fast.Response) -> typing.Mapping[str, str]:
    """Returns a fact about a kit."""
    fact: str = "Cats are amazing."
    return {"fact": fact}

