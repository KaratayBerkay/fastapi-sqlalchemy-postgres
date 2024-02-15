from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Index,
    Boolean,
    String,
    Integer,
    TIMESTAMP,
    Enum,
    text,
    ForeignKey,
    Numeric,
)
from sqlalchemy.dialects.postgresql import UUID, BYTEA, JSONB
from sqlalchemy.orm import relationship, mapped_column
from models.mixin import CrudCollection


class ExampleModel(CrudCollection):
    __tablename__ = "example_model"

    example_name = mapped_column(String, nullable=False)
    example_description = mapped_column(String, nullable=False)
    example_status = mapped_column(
        Enum("active", "inactive"), nullable=False, default="active"
    )
    example_data = mapped_column(JSONB, nullable=True)
    example_location = mapped_column(String, nullable=True)
    example_date = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    example_reference = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("example_reference.uu_id"),
        server_default=text("gen_random_uuid()"),
        nullable=True,
    )

    __table_args__ = (
        Index(
            "example_model_ndx_01",
            example_name,
            example_status,
        ),
        Index("example_model_ndx_02", example_date),
    )
