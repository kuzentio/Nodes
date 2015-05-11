from django import forms


class NodeEditForm(forms.Form):
    name = forms.CharField(initial='Name:')
