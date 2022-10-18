from sqlalchemy import types
from sqlalchemy.dialects.postgresql import TSVECTOR


class TSVector(types.TypeDecorator):
    impl = TSVECTOR
