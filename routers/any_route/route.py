from fastapi.routing import APIRouter
from models import ExampleModel
from pydantics import PydanticModel


any_route = APIRouter(prefix="/any_route", tags=["Any Route"])
any_route.include_router(any_route, include_in_schema=False)


@any_route.post(
    path="/list",
    summary="List Model Sqlalchemy",
)
def identifications_gateway_list(data: PydanticModel):
    data, count = ExampleModel.filter(data)
    return {"data": data, "count": count}
