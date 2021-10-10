import typing

__all__: list[str] = [
    "__version__",
    "__author__",
    "__description__",
    "__license__",
    "__maintainer__",
    "__url__",
    "__appdata__",
]

__version__: str = "0.1.0"
__author__: str = "Jonxslays"
__description__: str = "An api dedicated to kits."
__license__: str = "BSD-3-Clause"
__maintainer__: str = "Jonxslays"
__url__: str = "https://github.com/Jonxslays/kit-api"
__appdata__: dict[str, typing.Any] = {
    "title": "Kit API",
    "description": "An api dedicated to kits.",
    "version": __version__,
    "redoc_url": None,
    "contact": {"admin": "admin@kit-api.com"},
    "openapi": None,
}
