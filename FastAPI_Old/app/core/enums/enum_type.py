from sqlalchemy.types import TypeDecorator, Integer
from enum import IntFlag
from typing import Type

class IntFlagEnumType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_class: Type[IntFlag], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        return int(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return self.enum_class(value) if value is not None else None