import os
from datetime import datetime

from app.custom_classes import MacAddress
from app.schemas import Event

APPLICATION_NAME: str = "device-events-display"
JWT_PUBLIC_KEY_SECRETS_ID: str = (
    f'{os.path.join(APPLICATION_NAME, os.environ.get("ENVIRONMENT"), "public-key")}'
    if os.environ.get("ENVIRONMENT")
    else f'{os.path.join(APPLICATION_NAME, "public-key")}'
)
JWT_PUBLIC_KEY: str = os.environ.get("JWT_PUBLIC_KEY")
JWT_ISSUING_ENTITY: str = "mycompany.io"
JWT_AUDIENCE: str = "mygroup"
JWT_ALGORITHM: str = "RS512"

FAKE_DEVICE_MAC_ADDRESS: MacAddress = MacAddress("abcdef123456")
FAKE_PARENT_DEVICE_MAC_ADDRESS: MacAddress = MacAddress("001122334455")
FAKE_DOMAIN: str = "multiverse"
FAKE_EVENT: Event = Event(
    device_mac_address=FAKE_DEVICE_MAC_ADDRESS,
    parent_device_mac_address=FAKE_PARENT_DEVICE_MAC_ADDRESS,
    timestamp=datetime.now().timestamp(),
    device_domain=FAKE_DOMAIN,
)
