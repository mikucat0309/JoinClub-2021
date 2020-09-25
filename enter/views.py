from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AttendForm, CheckinForm
from .models import Attend, Checkin

def attend(request):
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '提交成功', extra_tags='attendform')
            return HttpResponseRedirect(reverse('commingsoon'))
    else:
        form = AttendForm()
    return render(request, 'attend.html', {'form': form})

@login_required
def search(request):
    if request.method == 'POST':
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        if nid:
            try:
                attend = Attend.objects.get(nid=nid)
                return render(request, 'enter_search.html', {'attend': attend})
            except Attend.DoesNotExist:
                return render(request, 'enter_search.html', {})
        elif name:
            try:
                attend = Attend.objects.get(name=name)
                return render(request, 'enter_search.html', {'attend': attend})
            except Attend.DoesNotExist:
                return render(request, 'enter_search.html', {})
    return render(request, 'enter_search.html', {})

@login_required
def edit(request, id):
    attend = get_object_or_404(Attend, id=id)
    if request.method == 'POST':
        form = AttendForm(request.POST, instance=attend)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'enter_edit.html', {'form': form, 'attend': attend})
    else:
        form = AttendForm()
    return render(request, 'enter_edit.html', {'form': form, 'attend': attend})

@login_required
def checkin(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            nid = form.cleaned_data['nid']
            if Attend.objects.filter(nid=nid).exists(): # status = 尚未領獎
                obj = form.save(commit=False)
                obj.status = 'YET'
                obj.save()
            else: # status = 無法領獎
                form.save()
            return HttpResponseRedirect(reverse('enter:prize', args=[nid]))
        else:
            return render(request, 'checkin.html', {'form': form})
    else:
        form = CheckinForm()
    return render(request, 'checkin.html', {'form': form})

@login_required
def prize(request, nid):
    attend = get_object_or_404(Checkin, nid=nid)
    if request.method == 'POST':
        if attend.status == 'NO' and ('tix' in request.POST):
            attend.status = 'TIX'
            attend.save()
        elif attend.status == 'YET':
            if 'confirm' in request.POST:
                attend.status = 'FORM'
                attend.save()
            elif 'mix' in request.POST:
                attend.status = 'MIX'
                attend.save()
    return render(request, 'prize.html', {'attend': attend})

def review(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        if member.status == 'UR':
            member.status = 'NP'
            member.save()
        elif member.status == 'NP':
            member.status = 'M'
            member.save()
    return render(request, 'review.html', {'member': member})
