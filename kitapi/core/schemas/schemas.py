from pydantic import BaseModel

__all__: list[str] = [
    "System",
    "Fact",
    "FactIn",
    "BulkFact",
    "BulkFactIn",
]


class System(BaseModel):
    """Represents the system."""

    version: int
    total_requests: int

    class Config:
        orm_mode = True


class Fact(BaseModel):
    """Represents a fact."""

    id: int
    fact: str
    uses: int

    class Config:
        orm_mode = True


class FactIn(BaseModel):
    """Represents a fact in."""

    fact: str

    class Config:
        orm_mode = True


class BulkFact(BaseModel):
    """Represents bulk facts."""

    facts: list[Fact]

    class Config:
        orm_mode = True


class BulkFactIn(BaseModel):
    """Represents bulk fact in."""

    facts: list[FactIn]

    class Config:
        orm_mode = True
