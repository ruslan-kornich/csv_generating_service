from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.forms import SchemaColumnsForm, SchemaBasicInfoForm
from app.models import SchemaBasicInfo, SchemaColumns


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
def data_sets(request, id):
    pass
