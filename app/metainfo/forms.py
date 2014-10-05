from django import forms

from metainfo.models import Domain


class DomainForm(forms.ModelForm):

    class Meta:
        model = Domain
        fields = ['domain']
