from django.forms import ModelForm
from .models import AlarmAsset

class AlarmAssetForm(ModelForm):
    class Meta:
        model = AlarmAsset
        fields = '__all__'
