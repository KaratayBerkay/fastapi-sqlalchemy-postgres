from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin
from sqlalchemy import func, TIMESTAMP, UUID, String, text, Any
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import session, Base
from .base import CrudMixin


class BaseCollection(Base, CrudMixin, ReprMixin, SerializeMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__

    id: Mapped[int] = mapped_column(primary_key=True)


class CrudCollection(Base, CrudMixin, ReprMixin, SmartQueryMixin, SerializeMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__

    id: Mapped[int] = mapped_column(primary_key=True)
    uu_id: Mapped[Any] = mapped_column(
        UUID(as_uuid=True), server_default=text("gen_random_uuid()"), index=True
    )
    # replication_id = Column(SmallInteger, server_default="0")
    ref_id: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[str] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[str] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


CrudCollection.set_session(session)
