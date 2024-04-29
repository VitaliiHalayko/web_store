from django.shortcuts import render

def categories(request):
    content = {}
    return render(request, 'categories/categories.html', content)
