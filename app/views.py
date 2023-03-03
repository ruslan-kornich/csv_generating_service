import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_celery_results.models import TaskResult

from app.forms import SchemaColumnsForm, SchemaBasicInfoForm
from app.models import SchemaBasicInfo, SchemaColumns, DataSets
from app.tasks import write_to_csv


def redirect_views(request):
    return redirect("/auth/login")


@login_required(login_url="/auth/login/")
def data_schemas(request):
    context = {}
    req_user = request.user
    query = SchemaBasicInfo.objects.filter(creator=req_user)
    context["request_user"] = req_user
    context["query"] = query
    return render(request, "app/data_schemas.html", context=context)


@login_required(login_url="/auth/login/")
def new_schema(request):
    context = {}
    form_column_schema = SchemaColumnsForm()
    form_basic_schema_info = SchemaBasicInfoForm()
    req_user = request.user
    query = SchemaBasicInfo.objects.filter(creator=req_user)
    context["request_user"] = req_user
    context["query"] = query
    context["form_column_schema"] = form_column_schema
    context["form_basic_schema_info"] = form_basic_schema_info
    return render(request, "app/new_schema.html", context=context)


@login_required
def add_new_schema(request):
    schema_name = request.POST.get("schema_name")
    column_separator = request.POST.get("column_separator")
    string_character = request.POST.get("string_character")

    name_column = request.POST.getlist("name_column")
    column_type = request.POST.getlist("column_type")
    int_from = request.POST.getlist("int_from")
    int_to = request.POST.getlist("int_to")
    sentences_number = request.POST.getlist("sentences_number")
    order = request.POST.getlist("order")

    new_schema = SchemaBasicInfo(
        schema_name=schema_name,
        column_separator=column_separator,
        string_character=string_character,
        creator=request.user,
    )
    new_schema.save()

    for item in range(0, len(name_column)):
        new_column = SchemaColumns.objects.create(
            schema=new_schema,
            column_name=name_column[item],
            column_type=column_type[item],
            int_from=int_from[item],
            int_to=int_to[item],
            sentences_number=sentences_number[item],
            order=order[item],
        )
        new_column.save()
    return redirect("/data-schemas")


@login_required(login_url="/auth/login/")
def edit_schema(request, id):
    context = {}
    form_column_schema = SchemaColumnsForm()
    form_basic_schema_info = SchemaBasicInfoForm()
    req_user = request.user
    columns = SchemaColumns.objects.filter(schema__id=id)
    query = SchemaBasicInfo.objects.get(id=id)
    context["request_user"] = req_user
    context["query"] = query
    context["columns"] = columns
    context["form_column_schema"] = form_column_schema
    context["form_basic_schema_info"] = form_basic_schema_info
    return render(request, "app/edit_schema.html", context=context)


@login_required(login_url="/auth/login/")
def delete_schema(request, id):
    query = SchemaBasicInfo.objects.get(id=id)
    query.delete()
    return redirect("/data-schemas")


@login_required(login_url="/auth/login/")
def update_schema(request, id):
    schema_name = request.POST.get("schema_name")
    column_separator = request.POST.get("column_separator")
    string_character = request.POST.get("string_character")

    name_column = request.POST.getlist("name_column")
    column_type = request.POST.getlist("column_type")
    int_from = request.POST.getlist("int_from")
    int_to = request.POST.getlist("int_to")
    sentences_number = request.POST.getlist("sentences_number")
    order = request.POST.getlist("order")

    schema = SchemaBasicInfo.objects.get(id=id)
    schema.schema_name = (str(schema_name),)
    schema.column_separator = (column_separator,)
    schema.string_character = (string_character,)
    schema.save()

    columns = SchemaColumns.objects.filter(schema=schema)
    for column in columns:
        column.delete()
    for item in range(0, len(name_column)):
        new_column = SchemaColumns.objects.create(
            schema=schema,
            column_name=name_column[item],
            column_type=column_type[item],
            int_from=int_from[item],
            int_to=int_to[item],
            sentences_number=sentences_number[item],
            order=order[item],
        )
        new_column.save()
    return redirect("/data-schemas")


@login_required(login_url="/auth/login/")
def data_sets(request, id):
    context = {}
    req_user = request.user
    schema = SchemaBasicInfo.objects.get(id=id)
    query = DataSets.objects.filter(schema__id=id)
    for item in query:
        try:
            task_status = TaskResult.objects.get(task_id=item.task_id).status
        except:
            task_status = "PENDING"
        item.task_status = task_status
        if item.task_status == "SUCCESS":
            item.status = "ready"
        else:
            item.status = "on process"
        item.save()

    context["request_user"] = req_user
    context["query"] = query
    context["schema"] = schema

    return render(request, "app/data_sets.html", context=context)


@login_required(login_url="/auth/login/")
def generate_data_views(request, id):
    schema_id = id
    rows_number = int(request.GET.get("rows_number"))
    schema = SchemaBasicInfo.objects.get(id=schema_id)

    folder_csv_file_path = "media/" + str(datetime.now().strftime("%Y-%m-%d"))
    create_new_folder(folder_csv_file_path)

    number_of_datasets = DataSets.objects.filter(schema=schema).count()
    csv_file_path = (
            folder_csv_file_path
            + "/"
            + schema.schema_name
            + str(number_of_datasets)
            + ".csv"
    )

    data = write_to_csv.delay(csv_file_path, schema_id, rows_number)

    dataset_model = DataSets(
        schema=schema,
        status="process",
        csv_file=csv_file_path,
        rows_number=rows_number,
        task_id=data.task_id,
    )
    dataset_model.save()
    return redirect("/data-sets/" + str(schema.id))


def create_new_folder(local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    return local_dir


@login_required(login_url="/auth/login/")
def generate_data(request, id):
    schema_id = id
    rows_number = int(request.GET.get("rows_number"))
    schema = SchemaBasicInfo.objects.get(id=schema_id)

    folder_csv_file_path = "media/" + str(datetime.now().strftime("%Y-%m-%d"))
    create_new_folder(folder_csv_file_path)

    number_of_datasets = DataSets.objects.filter(schema=schema).count()
    csv_file_path = (
            folder_csv_file_path
            + "/"
            + schema.schema_name
            + str(number_of_datasets)
            + ".csv"
    )

    data = write_to_csv.delay(csv_file_path, schema_id, rows_number)

    dataset_model = DataSets(
        schema=schema,
        status="process",
        csv_file=csv_file_path,
        rows_number=rows_number,
        task_id=data.task_id,
    )
    dataset_model.save()
    return redirect("/data-sets/" + str(schema.id))
