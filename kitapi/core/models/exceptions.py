__all__: list[str] = [
    "KitapiError",
    "MissingMasterKey",
]

class KitapiError(Exception):
    ...


class MissingMasterKey(KitapiError):
    ...
