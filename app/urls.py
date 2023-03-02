from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect_views, name="redirect_login"),
    path("data-schemas", views.data_schemas, name="data_schemas"),
    path("new-schema", views.new_schema, name="new_schema"),
    path("add-schema", views.add_new_schema, name="add_new_schema"),
]
