from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def comingsoon(request):
    return render(request, 'comingsoon.html', {})

def course(request):
    return render(request, 'course.html', {})

def error_400(request, exception):
    return render(request,'errors/400.html', {})

def error_403(request, exception):
    return render(request,'errors/403.html', {})

def error_404(request, exception):
    return render(request,'errors/404.html', {})

def error_500(request):
    return render(request,'errors/500.html', {})

def csrf_failure(request, reason=""):
    return render(request,'errors/403_csrf.html', {})
