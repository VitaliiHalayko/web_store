from django.shortcuts import render
from .models import Categories

def categories(request):
    content = Categories.objects.all()
    return render(request, 'categories/categories.html', {'categories': content})
