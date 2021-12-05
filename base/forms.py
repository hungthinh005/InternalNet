from django.forms import ModelForm
from .models import Function

class MeetingForm(ModelForm):
    class Meta:
        model = Function
        fields = '__all__'