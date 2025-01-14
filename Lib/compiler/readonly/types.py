from __future__ import annotations

from typing import List


class Value:
    def __init__(self, is_readonly: bool, bases: List[Value], name: str) -> None:
        """
        is_readonly: the Value is readonly and cannot be modified
        """
        self.is_readonly = is_readonly
        self.bases = bases
        self.name = name

    def can_convert_to(self, other: Value) -> bool:
        return other is self or other in self.bases

    def __str__(self) -> str:
        return self.name


class FunctionValue:
    def __init__(
        self,
        readonly_nonlocal: bool,
        returns_readonly: bool,
        yields_readonly: bool,
        sends_readonly: bool,
        args: List[Value],
    ) -> None:
        self.readonly_nonlocal = readonly_nonlocal
        self.returns_readonly = returns_readonly
        self.yields_readonly = yields_readonly
        self.sends_readonly = sends_readonly
        self.args = args

READONLY = Value(True, [], "readonly")
MUTABLE = Value(False, [READONLY], "mutable")
