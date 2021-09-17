from typing import Counter
from django.db import models


class Member(models.Model):
    LEVEL_CHOICES = [
        ('B1', '大一'),
        ('B2', '大二'),
        ('B3', '大三'),
        ('B4', '大四'),
        ('M1', '碩一'),
        ('M2', '碩二'),
    ]

    STATUS_CHOICES = [
        ('NP', '未付款'),
        ('M', '已入社'),
    ]

    PAY_CHOICES = [
        ('C', '現金'),
        ('R', '匯款'),
    ]

    SCHOOL_CHOICES = [
        ('Y', '逢甲大學'),
        ('N', '其他學校'),
    ]

    CLOTHES_CHOICES = [
        ('N', '不購買'),
        ('S', '尺寸S'),
        ('M', '尺寸M'),
        ('L', '尺寸L'),
        ('XL', '尺寸XL'),
    ]

    CLOTHES_STATUS_CHOICES = [
        ('N', '不購買'),
        ('NG', '未領取'),
        ('G', '已領取'),
    ]

    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)
    dept = models.CharField(max_length=20)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='B1')
    # 不能用 unique=True，因為空字串也會被判斷成一樣
    phone = models.CharField(max_length=15, null=True, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default="NP")
    pay = models.CharField(max_length=2, choices=PAY_CHOICES, default="C")
    bankAccount = models.CharField(max_length=5, null=True, blank=True)
    is_FCU = models.CharField(max_length=5, choices=SCHOOL_CHOICES,default="Y")
    school = models.CharField(max_length=50, blank=True)
    DiscordId = models.CharField(max_length=50, blank=True)
    clothes = models.CharField(max_length=4, choices=CLOTHES_CHOICES, default='N')
    clothes_status = models.CharField(max_length=3, choices=CLOTHES_STATUS_CHOICES, default='N')
    def __str__(self):
        return "%s %s [%s]" % (self.nid, self.name, self.get_status_display())


class secret(models.Model):
    """
    保密協議
    """
    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, null=True,
                             unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

class receipt(models.Model):
    """
    紀錄收據的編號
    """
    count = models.IntegerField()