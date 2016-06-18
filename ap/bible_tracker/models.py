from django.db import models
from django.contrib.postgres.fields import HStoreField
from accounts.models import User

class BibleReading(models.Model):
    trainee = models.ForeignKey(User, null=True)
    weekly_reading_status = HStoreField()
    books_read = HStoreField()