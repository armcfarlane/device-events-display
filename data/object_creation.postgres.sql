DROP DATABASE IF EXISTS devices;
CREATE DATABASE devices;

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    device_mac_address macaddr PRIMARY KEY,
    device_domain VARCHAR(255) NOT NULL,
    parent_device_mac_address macaddr,
    creation_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    creation_date DATE
)
PARTITION BY RANGE(creation_date);

DROP TABLE IF EXISTS latest_events;
CREATE TABLE latest_events (
    device_mac_address macaddr PRIMARY KEY,
    device_domain VARCHAR(255) NOT NULL,
    parent_device_mac_address macaddr,
    creation_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
)
