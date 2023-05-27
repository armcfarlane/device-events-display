from pydantic import BaseModel

from app.custom_classes import MacAddress


# Create the events schema
class Event(BaseModel):
    device_mac_address: MacAddress
    parent_device_mac_address: MacAddress
    timestamp: float
    device_domain: str


# Create the recent_events schema
class RecentEvent(BaseModel):
    device_mac_address: MacAddress
    parent_device_mac_address: MacAddress
    timestamp: float
    device_domain: str
