from collections.abc import Callable
from typing import Any, Concatenate, ParamSpec, TypeVar, overload

UpdateT = TypeVar("UpdateT")
FacadeT = TypeVar("FacadeT")
RT = TypeVar("RT")
P = ParamSpec("P")


@overload
def promote(
    method: Callable[Concatenate[FacadeT, P], RT],
) -> Callable[Concatenate[UpdateT, P], RT]: ...

@overload
def promote(method: Callable[[FacadeT], RT]) -> Callable[[UpdateT], RT]: ...

@overload
def promote(method: Callable[..., RT]) -> Callable[..., RT]: ...

def promote(method: Any) -> Any:
    raise RuntimeError("This function should only be used for type checking")
