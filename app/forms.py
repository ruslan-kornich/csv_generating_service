from django import forms

from app.models import SchemaColumns, SchemaBasicInfo


class SchemaColumnsForm(forms.ModelForm):
    class Meta:
        model = SchemaColumns
        fields = "__all__"


class SchemaBasicInfoForm(forms.ModelForm):
    class Meta:
        model = SchemaBasicInfo
        fields = "__all__"
