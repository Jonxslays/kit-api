from tortoise import fields, models

__all__: list[str] = [
    "Fact",
    "System",
]


class Fact(models.Model):
    """Facts table."""

    id: int = fields.IntField(pk=True)
    fact: str = fields.TextField()
    uses: int = fields.BigIntField(default=0)


class System(models.Model):
    """System table."""

    version: int = fields.IntField(pk=True)
    total_requests: int = fields.BigIntField(default=1)
