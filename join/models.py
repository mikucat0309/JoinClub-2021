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
        ('UR', '審核中'), 
        ('M', '已入社'),
        ('NP', '未付款'),
    ]

    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)
    dept = models.CharField(max_length=20)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True) # 不能用 unique=True，因為空字串也會被判斷成一樣
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="UR")

    def __str__(self):
        return "%s %s [%s]" % (self.nid, self.name, self.get_status_display())

