# flake8: noqa
if False:
    from .promise import Promise
    from typing import Iterator


def iterate_promise(promise):
    # type: (Promise) -> Iterator
    from ...libraries.promise import future
    if not promise.is_fulfilled:
        yield from future  # type: ignore
    assert promise.is_fulfilled
    return promise.get()
