from django.shortcuts import render
from .models import Category


def categories(request):
    """
    Renders the categories page

    :param request: request from user
    :return: the categories page
    """
    content = Category.objects.all()
    print(content)
    return render(request, 'categories/categories.html', {
        'categories': content
    })
