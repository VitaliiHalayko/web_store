from django.shortcuts import render
from .models import Category

def categories(request):
    content = Category.objects.all()
    return render(request, 'categories/categories.html', {
        'active': 'shop',
        'categories': content
    })
