from django.shortcuts import render, redirect


def home(request):
    return render(request,'home.html')


def home_redirect(request):
    return redirect('home')