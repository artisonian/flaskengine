import datetime
import mongoengine

class Entry(mongoengine.Document):
    """An Entry document model."""
    title = mongoengine.StringField(required=True, max_length=200)
    text = mongoengine.StringField()
    created_at = mongoengine.DateTimeField(
        default=datetime.datetime.now())