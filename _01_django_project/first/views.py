from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def greeting(request):
    return HttpResponse("<h1>안녕 장고!! 👍😘</h1>")

def foo(request):
    return HttpResponse('<h1>🦑Foooooooooooooooooooo🦑</h1>')


def bar(request):
    return HttpResponse('''
    <html>
    <head>
      <title>🐳Bar Page🐳</title>
    </head>
    <body>
      <h1>🐳Bar Page🐳</h1>
      <p>🐳This is a bar page🐳</p>
    </body>
    </html>
    ''')
