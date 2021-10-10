__all__: list[str] = [
    "DatabaseConnectionError",
    "KitapiError",
    "MissingMasterKey",
]


class KitapiError(Exception):
    ...


class MissingMasterKey(KitapiError):
    ...


class DatabaseConnectionError(KitapiError):
    ...
