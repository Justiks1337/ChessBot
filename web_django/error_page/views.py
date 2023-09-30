from django.shortcuts import render
from django.http import HttpRequest


def handler404(request: HttpRequest, *args, **kwargs):
    return render(request, 'error_page/index.html', {'error_number': "404"})
