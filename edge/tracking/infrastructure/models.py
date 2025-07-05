from peewee import Model, AutoField, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db

class TrackingRecord(Model):
    id = AutoField()
    device_id = CharField()
    latitude = FloatField()
    longitude = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = "tracking_records"
