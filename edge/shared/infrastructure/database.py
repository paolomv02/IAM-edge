"""
Database initialization for Edugo Edge Service.

Sets up the SQLite database and creates required tables for TrackingRecord.
"""

from peewee import SqliteDatabase

# Initialize SQLite database
db = SqliteDatabase('edugo_edge.db')

def init_db() -> None:
    """
    Initialize the database and create tables for Device model.
    """
    if db.is_closed():
        db.connect()

    # Existence check for Device model
    from tracking.infrastructure.models import TrackingRecord
    from iam.infrastructure.models import Device

    db.create_tables([TrackingRecord], safe=True)
    db.create_tables([Device], safe=True)

    db.close()
