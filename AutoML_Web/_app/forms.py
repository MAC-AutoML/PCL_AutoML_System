from django import forms
from django.core.exceptions import ValidationError
from . import models

# 待完善
class job_form(forms.Form):
    name=forms.CharField(min_length=2,label="Model name",error_messages=
    {
        "min_length":"Model name too short!",
        "required":"This field must be filled!"
    }
    )
