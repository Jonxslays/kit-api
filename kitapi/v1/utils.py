import functools
import os
import typing

from kitapi.core import models


@functools.lru_cache
def get_master_key() -> str:
    """Gets the V1 master key from the environment."""
    key: typing.Optional[str] = os.environ.get("V1_MASTER_KEY")

    if key is not None:
        return key

    raise models.MissingMasterKey("No API master key was found in the environment.")
