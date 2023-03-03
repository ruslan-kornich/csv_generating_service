from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from app.services.data_choices import (
    SEPARATOR_CHOICES,
    STRING_CHARACTER_CHOICES,
    TYPE_CHOICES,
    STATUS_CHOICES,
)


class BaseModel(models.Model):
    created_time = models.DateTimeField(db_index=True, default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SchemaBasicInfo(BaseModel):
    schema_name = models.CharField(max_length=20, null=True)
    column_separator = models.CharField(
        max_length=15, choices=SEPARATOR_CHOICES, default=";"
    )
    string_character = models.CharField(
        max_length=15, choices=STRING_CHARACTER_CHOICES, default="'"
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


class SchemaColumns(BaseModel):
    column_name = models.CharField(max_length=20, default="", null=True)
    column_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="full_name"
    )
    schema = models.ForeignKey(SchemaBasicInfo, on_delete=models.CASCADE, null=True)
    int_from = models.PositiveIntegerField(default=0, null=True)
    int_to = models.PositiveIntegerField(default=0, null=True)
    sentences_number = models.PositiveIntegerField(default=0, null=True)
    order = models.PositiveIntegerField(default=0, null=False)

    def __str__(self):
        return str(self.column_name)


class DataSets(BaseModel):
    schema = models.ForeignKey(SchemaBasicInfo, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="process")
    csv_file = models.CharField(max_length=300, default="", null=True)
    rows_number = models.PositiveIntegerField(default=0, null=True)
    task_id = models.CharField(max_length=300, default="", null=True)
    task_status = models.CharField(max_length=40, default="", null=True)

    def __str__(self):
        return str(self.schema)
