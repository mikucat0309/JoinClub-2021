from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JoinForm
from .models import Member
from enter.models import Attend

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '提交成功', extra_tags='joinform')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = JoinForm()
    return render(request, 'join.html', {'form': form})

@login_required
def search(request):
    if request.method == 'POST':
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        if nid:
            try:
                member = Member.objects.get(nid=nid)
                return HttpResponseRedirect(reverse('join:review', args=[member.id]))
            except Member.DoesNotExist:
                return render(request, 'join_search.html', {})
        elif name:
            try:
                member = Member.objects.get(name=name)
                return HttpResponseRedirect(reverse('join:review', args=[member.id]))
            except Member.DoesNotExist:
                return render(request, 'join_search.html', {})
    return render(request, 'join_search.html', {})

@login_required
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


