from django.shortcuts import render, redirect

# Create your views here.

def homeF(request):
    return render(request, 'front/homeF.html')