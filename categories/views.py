from django.shortcuts import render
from .models import Category


def categories(request):
    content = Category.objects.all()
    print(content)
    return render(request, 'categories/categories.html', {
        'categories': content
    })
