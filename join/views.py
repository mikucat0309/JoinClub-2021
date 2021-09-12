from typing import Counter
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.query_utils import Q
from .forms import JoinForm, secretForm
from .models import Member, secret, receipt
from enter.models import Attend
from .mail import word, mail
from django.utils import timezone
import os


def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 '提交成功', extra_tags='joinform')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = JoinForm()
    return render(request, 'join.html', {'form': form})


def join_secret(request):
    """
    填寫保密協議表單
    """
    if request.method == 'POST':
        form = secretForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 '提交成功', extra_tags='secretform')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = secretForm()
    return render(request, 'secretForm.html', {'form': form})


def searchForMember(request):
    """
    給社員們用來查詢自己的繳費情形
    """
    if request.method == 'POST':
        nid = request.POST.get('nid')
        if nid:
            try:
                member = Member.objects.get(nid=nid)
                return render(request, 'searchForMember.html', {'member': member})
            except Member.DoesNotExist:
                return render(request, 'searchForMember.html', {'result': '無搜尋結果'})
    return render(request, 'searchForMember.html', {})

# TODO edit review表單跟顯示都還要改 還有autoPEP8
# TODO 條碼機搜尋保密協議 OK
# TODO 寄送收據
# TODO 入社表單多一個勾選框 寫說入社需同意保密協議 OK
# TODO 入社表單 在注意事項按鈕旁邊再加個按鈕顯示（？ 顯示保密協議
# TODO 學生證刷條碼機的部分 綠色 紅色 OK
# TODO 修改requirment doc2pdf
# TODO 修改注意事項


@login_required
def search(request):
    """
    admin搜尋入社表單
    """
    if request.method == 'POST':
        searchTerm = request.POST.get('searchTerm')
        # 搜尋大雜燴 一個關鍵字 全部欄位都搜尋
        members = Member.objects.filter(Q(name__icontains=searchTerm) |
                                        Q(nid__icontains=searchTerm) |
                                        Q(dept__icontains=searchTerm) |
                                        Q(phone__icontains=searchTerm) |
                                        Q(email__icontains=searchTerm))
        # print(members)
        context = {'members': members}
        return render(request, 'join_search.html', context)
        # nid = request.POST.get('nid')
        # name = request.POST.get('name')
        # if nid:
        #     try:
        #         member = Member.objects.get(nid=nid)
        #         return HttpResponseRedirect(reverse('join:review', args=[member.id]))
        #     except Member.DoesNotExist:
        #         return render(request, 'join_search.html', {})
        # elif name:
        #     try:
        #         member = Member.objects.get(name=name)
        #         return HttpResponseRedirect(reverse('join:review', args=[member.id]))
        #     except Member.DoesNotExist:
        #         return render(request, 'join_search.html', {})
    return render(request, 'join_search.html', {})


@login_required
def secretSearch(request):
    """
    admin搜尋保密協議
    """
    if request.method == 'POST':
        searchTerm = request.POST.get('searchTerm')
        # 搜尋對應的學號
        # secretResult = secret.objects.filter(Q(nid__iexact=searchTerm))

        # 搜尋大雜燴 一個關鍵字 全部欄位都搜尋
        secrets = secret.objects.filter(Q(name__icontains=searchTerm) |
                                        Q(nid__icontains=searchTerm) |
                                        Q(phone__icontains=searchTerm))
        try:
            # 條碼機刷學生證會多一位數
            Temp = searchTerm
            if len(searchTerm) == 9:
                Temp = searchTerm[0:-1]
            secretResult = secret.objects.get(nid__iexact=Temp)
            context = {'secret': secretResult, 'secrets': secrets}
            return render(request, 'secret_search.html', context)
        except secret.DoesNotExist:
            context = {'secrets': secrets, 'searchTerm': searchTerm}
            return render(request, 'secret_search.html', context)

    return render(request, 'secret_search.html', {})


def send_email(id):
    '''
    繳費完成後，寄送收據給社員
    '''
    member = get_object_or_404(Member, id=id)
    if member.is_FCU == 'N':  # 校外學生
        return 0
    path = 'Receipt'
    file = os.path.join(path, member.nid + '.pdf')
    print(file)
    if os.path.isfile(file) == False:
        Receipt = receipt.objects.all()
        if len(Receipt) == 0:
            receipt.objects.create(count=1)
            Receipt = receipt.objects.all()
        receiptTmp = Receipt[0]

        time_now = timezone.now().strftime("%Y-%m-%d")
        year = timezone.now().strftime("%Y")
        # 202110101001
        # 2021年份 10101入社費會科 001 第一份
        num = year + "10101" + str(receiptTmp.count).zfill(3)
        word(member.name, member.nid, time_now, num)
        receiptTmp.count += 1
        receiptTmp.save()
    mail(member.name, member.nid)


@login_required
def review(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        if member.status == 'UR':
            member.status = 'NP'
            member.save()
        elif member.status == 'NP':
            member.status = 'M'
            # 狀態改為已入社 順便寄送電子收據
            send_email(id)
            member.save()
    return render(request, 'review.html', {'member': member})


@login_required
def edit(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = JoinForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('join:review', args=[member.id]))
        else:
            return render(request, 'join_edit.html', {'form': form, 'member': member})
    else:
        form = JoinForm()
    return render(request, 'join_edit.html', {'form': form, 'member': member})


@login_required
def view(request):
    M_members = Member.objects.filter(status='M')
    NP_members = Member.objects.filter(status='NP')
    UR_members = Member.objects.filter(status='UR')
    attends = Attend.objects.all()
    return render(request, 'view.html', {'M_members': M_members, 'NP_members': NP_members, 'UR_members': UR_members, 'attends': attends})
