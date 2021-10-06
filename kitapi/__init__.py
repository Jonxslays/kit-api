import typing

__all__: typing.List[str] = [
    "__version__",
    "__description__",
    "__author__",
    "__maintainer__",
    "__license__",
    "__url__",
    "__appdata__",
]

__version__: str = "0.1.0"
__description__: str = "An api dedicated to kits."
__author__: str = "Jonxslays"
__maintainer__: str = "Jonxslays"
__license__: str = "BSD-3-Clause"
__url__: str = "https://github.com/Jonxslays/kit-api"
__appdata__: typing.Mapping[str, typing.Optional[str]] = {
    "title": "Kit API",
    "description": "An api dedicated to kits.",
    "version": __version__,
    "redoc_url": None,
}
