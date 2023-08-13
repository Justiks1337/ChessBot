from django.shortcuts import render
from django.http import HttpRequest


def handler500(request: HttpRequest):
    return render(request, 'error_page/index.html', {'error_number': "404"})
