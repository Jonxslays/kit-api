from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator

__all__: list[str] = [
    "Fact",
    "Facts",
    "FactIn",
    "System",
    "Systems",
]


class Facts(models.Model):
    """Database model for a kit fact."""

    id: int = fields.IntField(pk=True)
    fact: str = fields.TextField()
    uses: int = fields.BigIntField(default=0)

    class PydanticMeta:
        pass


class Systems(models.Model):
    """System table."""

    version: int = fields.IntField(pk=True)
    total_requests: int = fields.BigIntField(default=1)

    class PydanticMeta:
        pass


Fact = pydantic_model_creator(Facts, name="Fact")
FactIn = pydantic_model_creator(Facts, name="FactIn", exclude=("uses",), exclude_readonly=True)

System = pydantic_model_creator(Systems, name="System")
