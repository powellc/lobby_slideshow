from django import forms
from tinymce.widgets import TinyMCE
from superslides.models import Slide

class SlideAdminForm(forms.ModelForm):
        text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)

        class Meta:
            model = Slide
