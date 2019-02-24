from django.shortcuts import render
from django.urls import reverse, reverse_lazy


def index(request):
    return render(request, 'index.html')