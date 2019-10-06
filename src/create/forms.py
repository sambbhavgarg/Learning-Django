from django import forms
import datetime

from .models import Banner

class InputForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = [
            'Input'
        ]
class RawProductForm(forms.Form):
    Input = forms.CharField(label = '', widget=forms.Textarea(attrs={
    	# "style": "text-align: center; padding-top: 45px;",
    	"placeholder": "Let yourself out.",
    	"class" : "textarea is-hover",
    	"id": "input_area",
    	"rows": 3
    	}))
