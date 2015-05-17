# -*- coding: utf-8 -*-
from Nodes.app.nodes import models
from django import forms


class NodeForm(forms.Form):
    name = forms.CharField(label='Название:', max_length=100)

    class Meta:
        model = models.Unit

class RelationsForm(forms.Form):
    pass


