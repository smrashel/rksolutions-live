from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def index(request):
    context = {}
    return render(request, 'portfolio/index.html', context)
