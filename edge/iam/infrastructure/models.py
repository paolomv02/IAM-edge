from peewee import Model, CharField, DateTimeField
from shared.infrastructure.database import db
from datetime import datetime

class Device(Model):
    """
    Represents an RFID bracelet registered in the system. Contains the unique RFID code
    and the API key that can be used by the mobile app to identify the student.
    """
    rfid_code = CharField(unique=True, max_length=64)  # generado automáticamente
    api_key = CharField(unique=True, max_length=64)    # generado automáticamente
    registered_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db
        table_name = 'devices'
