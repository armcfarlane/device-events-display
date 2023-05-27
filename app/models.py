import sqlalchemy
from custom_classes import MacAddress

# Create the metadata object
metadata = sqlalchemy.MetaData()

# Create the events table
events_table = sqlalchemy.Table(
    "events",
    metadata,
    sqlalchemy.Column(
        "device_mac_address",
        sqlalchemy.dialects.postgresql.MACADDR,
        primary_key=True,
    ),
    sqlalchemy.Column(
        "parent_device_mac_address", sqlalchemy.dialects.postgresql.MACADDR
    ),
    sqlalchemy.Column("timestamp", sqlalchemy.Float),
    sqlalchemy.Column("device_domain", sqlalchemy.String),
)

# Create the recent_events table
recent_events_table = sqlalchemy.Table(
    "recent_events",
    metadata,
    sqlalchemy.Column(
        "device_mac_address",
        sqlalchemy.dialects.postgresql.MACADDR,
        primary_key=True,
    ),
    sqlalchemy.Column(
        "parent_device_mac_address", sqlalchemy.dialects.postgresql.MACADDR
    ),
    sqlalchemy.Column("timestamp", sqlalchemy.Float),
    sqlalchemy.Column("device_domain", sqlalchemy.String),
)

# Create the engine
engine = sqlalchemy.create_engine("postgresql://localhost/device_events")

# Create the connection
connection = engine.connect()

# Create the metadata
metadata.create_all(engine)

# Create the events table
events = events_table.metadata.tables["events"]

# Create the recent_events table
recent_events = recent_events_table.metadata.tables["recent_events"]
