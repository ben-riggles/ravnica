from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    id: int = models.AutoField(primary_key=True)
    date_created: datetime = models.DateTimeField(auto_now_add=True)
    date_modified: datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True