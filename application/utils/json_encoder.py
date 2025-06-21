from datetime import datetime
from json import JSONEncoder
from uuid import UUID


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


_default_encoder = CustomJsonEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
)


def dumps(
    obj,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw,
):

    if (
        not skipkeys
        and ensure_ascii
        and check_circular
        and allow_nan
        and cls is None
        and indent is None
        and separators is None
        and default is None
        and not sort_keys
        and not kw
    ):
        return _default_encoder.encode(obj)
    if cls is None:
        cls = CustomJsonEncoder
    return cls(
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    ).encode(obj)
