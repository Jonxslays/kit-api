import typing

import fastapi as fast


router = fast.APIRouter()


@router.get("/fact", summary="Returns a fact about a kit.")
async def fact_endpoint(response: fast.Response, amount: int = 1) -> typing.Mapping[str, str]:
    fact: str = "Cats are amazing."

    if amount > 25:
        response.status_code = fast.status.HTTP_400_BAD_REQUEST
        return {
            "Error": "Bad Request",
            "Message": "You may only retrieve 25 facts per request."
        }

    if amount == 1:
        return {"fact": fact}

    output: typing.Mapping[str, str] = {}

    for i in range(amount):
        output[f"fact_{i + 1}"] = fact

    return output
