import os
from datetime import datetime
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from prometheus_fastapi_instrumentator import Instrumentator

from app import (FAKE_DOMAIN, FAKE_PARENT_DEVICE_MAC_ADDRESS, JWT_ALGORITHM,
                 JWT_AUDIENCE, JWT_ISSUING_ENTITY, JWT_PUBLIC_KEY)
from app.custom_classes import MacAddress
from app.dependencies import Authenticate
from app.schemas import Event

service_name: str = "Device Event Display"
app_description: str = f"""The {service_name} service allows you to retrieve messages pertaining to a device.
"""
openapi_tags: list[dict[str, Any]] = [
    {
        "name": "latest",
        "description": "Most recent (latest) device events",
    },
    {
        "name": "by-timeslice",
        "description": "device events by user-supplied datetime",
    },
]

app = FastAPI(
    title=service_name,
    description=app_description,
    version=os.environ.get("EVENTS_DISPLAY_IMAGE_VERSION", "0.0.0"),
    openapi_tags=openapi_tags,
)


@app.get(
    "/latest-events/{mac_address}",
    summary="Get Latest Device Event",
    description="Get a device's latest event",
    dependencies=[Depends(Authenticate())],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "The latest device event was returned successfully"},
        401: {"description": "The user could not be authenticated"},
        403: {
            "description": "The user was authenticated but does not have permission to use this endpoint"
        },
        404: {"description": "The device was not found, so no event was returned"},
        500: {"description": "Unhandled server error"},
    },
    tags=["latest"],
)
async def get(
    mac_address: MacAddress = Path(..., description="The device's mac address"),
    stubbed: bool = Query(
        False, description="If true, returned a stubbed (not real) response"
    ),
) -> Event:

    mac_address_dialect: str = "mac_unix_expanded"
    mac_address_case: str = "upper"

    if stubbed:
        return Event(
            device_mac_address=MacAddress(mac_address).format(
                dialect=mac_address_dialect,
                case=mac_address_case,
            ),
            parent_device_mac_address=MacAddress(FAKE_PARENT_DEVICE_MAC_ADDRESS).format(
                dialect=mac_address_dialect,
                case=mac_address_case,
            ),
            timestamp=datetime.now().timestamp(),
            device_domain=FAKE_DOMAIN,
        ).__dict__
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Getting a real (not stubbed) response has not yet been implemented",
        )
