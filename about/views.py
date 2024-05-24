from django.shortcuts import render


def about(request):
    """
    View function for the about page.

    Renders the about page.
    """
    return render(request, 'about/about.html')
