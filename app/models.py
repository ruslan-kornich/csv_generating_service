from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_time = models.DateTimeField(db_index=True, default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SchemaBasicInfo(BaseModel):
    SEPARATOR_CHOICES = (
        (",", "Comma(,)"),
        ("|", "Forward slash (|)"),
        (";", "Semicolon(;)"),
    )

    STRING_CHARACTER_CHOICES = (
        ('"', 'Double-quote(")'),
        ("'", "Single-quote(')"),
        ("'''", "Triple-quote(''')"),
        ('"""', 'Triple-quote(""")'),
        ('()', 'Bracket(())'),
        ('[]', 'Straight Brackets([])'),
    )
    schema_name = models.CharField(max_length=20, null=True)
    column_separator = models.CharField(max_length=15, choices=SEPARATOR_CHOICES, default=";")
    string_character = models.CharField(max_length=15, choices=STRING_CHARACTER_CHOICES, default="'")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


class SchemaColumns(BaseModel):
    TYPE_CHOICES = (
        ("full_name", "Full Name"),
        ("company", "Company"),
        ("address", "Address"),
        ("job", "Job"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("text", "Text"),
        ("int", "Integer"),
        ("date", "Date"),
    )
    column_name = models.CharField(max_length=20, default='', null=True)
    column_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="full_name")
    schema = models.ForeignKey(SchemaBasicInfo, on_delete=models.CASCADE, null=True)
    int_from = models.PositiveIntegerField(default=0, null=True)
    int_to = models.PositiveIntegerField(default=0, null=True)
    sentences_number = models.PositiveIntegerField(default=0, null=True)
    order = models.PositiveIntegerField(default=0, null=False)

    def __str__(self):
        return str(self.column_name)


class DataSets(BaseModel):
    STATUS_CHOICES = (
        ("ready", "ready"),
        ("process", "processing")
    )
    schema = models.ForeignKey(SchemaBasicInfo, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="In process")
    csv_file = models.CharField(max_length=300, default='', null=True)
    rows_number = models.PositiveIntegerField(default=0, null=True)
    task_id = models.CharField(max_length=300, default='', null=True)
    task_status = models.CharField(max_length=40, default='', null=True)

    def __str__(self):
        return str(self.schema)
