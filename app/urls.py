from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.redirect_views, name="redirect_views"),
    path('data-schemas', views.data_schemas, name="data_schemas"),
    path('new-schema', views.new_schema, name="new_schema"),
    path('edit-schema/<int:id>/', views.edit_schema, name="edit_schema"),
    path('delete-schema/<int:id>/', views.delete_schema, name="delete_schema"),
    path('add-schema', views.add_new_schema, name="adding_new_schema"),
    path('update-schema/<int:id>', views.update_schema, name="updating_schema"),
    path('data-sets/<int:id>', views.data_sets, name="data_sets"),
    path('generate/<int:id>/', views.generate_data, name="generate_data")
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)