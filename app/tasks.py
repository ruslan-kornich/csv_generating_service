import csv

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from faker import Faker

from app.models import SchemaColumns, SchemaBasicInfo

fake = Faker(["it_IT", "en_US"])


@shared_task(bind=True)
def write_to_csv(self, csv_file_path, schema_id, rows_number):
    columns = SchemaColumns.objects.filter(schema__id=schema_id)
    schema = SchemaBasicInfo.objects.get(id=schema_id)
    header = [column.column_name for column in columns]
    data = []
    for i in range(rows_number):
        row = []
        for column in columns:
            if column.column_type == "full_name":
                field = fake.name()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "address":
                field = fake.address()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "company":
                field = fake.company()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "job":
                field = fake.job()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "email":
                field = fake.email()
                row.append(field)

            elif column.column_type == "phone":
                field = fake.phone_number()
                row.append(field)

            elif column.column_type == "text":
                field = fake.paragraph(nb_sentences=column.sentences_number)
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "int":
                field = fake.random_int(min=column.int_from, max=column.int_to)
                row.append(field)

            elif column.column_type == "date":
                field = fake.date()
                row.append(field)
        data.append(row)

    progress_recorder = ProgressRecorder(self)
    for i in range(5):
        progress_recorder.set_progress(i + 1, 5, f"On iteration{i}")

    with open(csv_file_path, "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(
            f,
            delimiter=schema.column_separator,
            lineterminator="\r\n",
            quotechar=get_quotation_marks(schema.string_character),
        )
        writer.writerow(header)
        writer.writerows(data)
    return "Done"


def get_quotation_marks(string_character):
    if string_character in ['"', '"""']:
        return "'"

    if string_character in ["'", "'''"]:
        return '"'


def get_string(string_character, field):
    if string_character in ["()", "[]"]:
        string = string_character[-2] + field + string_character[-1]
    else:
        string = string_character + field + string_character
    return string
