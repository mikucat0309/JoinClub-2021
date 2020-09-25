from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import Member
import re

LEVEL_CHOICES = (
    ('B1', '大一'),
    ('B2', '大二'),
    ('B3', '大三'),
    ('B4', '大四'),
    ('M1', '碩一'),
    ('M2', '碩二')
)

class JoinForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'nid', 'dept', 'level', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入姓名'}),
            'nid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入學號'}),
            'dept': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'deptHelp', 'placeholder': '請輸入系級'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'phoneHelp', 'placeholder': '請輸入電話號碼'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': '請輸入電子郵件'}),
        }
        labels = {
            'name': _('姓名'),
            'nid': _('學號'),
            'dept': _('系級'),
            'level': _('年級'),
            'phone': _('電話'),
            'email': _('E-mail'),
        }
        help_texts = {
            'dept': _('例如:資訊一甲'),
            'phone': _('請輸入可以聯絡到您的手機'),
            'email': _('請輸入您常用的 E-mail'),
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
            'dept': {
                'required': _('必須填寫系級'),
                'max_length': _('你的系級太長囉'),
            },
            'level': {
                'required': _('必須選擇年級'),
                'invalid_choice': _('請勿亂來'),
            },
            'phone': {
                'max_length': _('你的電話太長囉'),
                'unique': _('您的手機號碼已經被使用過囉'),
            },
            'email': {
                'required': _('必須填寫 E-mail'),
                'unique': _('您的 Email 已經被使用過囉'),
                'invalid': _('您的 E-mail 看起來怪怪的喔')
            },
        }

