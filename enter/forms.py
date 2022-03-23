from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Attend, Checkin

class AttendForm(ModelForm):
    class Meta:
        model = Attend
        fields = ['name', 'nid']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入姓名'}),
            'nid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入學號'})
        }
        labels = {
            'name': _('姓名'),
            'nid': _('學號'),
        }
        error_messages = {
            'name': {
                'required': _('必須填寫姓名'),
                'max_length': _('你的姓名太長囉'),
            },
            'nid': {
                'required': _('必須填寫學號'),
                'unique': _('您的學號已經被使用過囉'),
                'max_length': _('你的學號太長囉'),
            },
        }

class CheckinForm(ModelForm):
    class Meta:
        model = Checkin
        fields = ['nid']
        widgets = {
            'nid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入欲簽到學號'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nid': _('學號'),
            'status': _('領獎狀態'),
        }
        error_messages = {
            'nid': {
                'required': _('必須填寫學號'),
                'unique': _('您的學號已經簽到'),
                'max_length': _('你的學號太長囉'),
            },
            'status': {
                'invalid_choice': _('請勿亂來'),
            },
        }
