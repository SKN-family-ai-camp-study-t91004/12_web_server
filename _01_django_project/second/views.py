from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# render(request, 'templates/ 하위 html 경로' [,context=None])
# - settings.py에 등록된 TEMPLATES의 DIRS 경로(templates/)를
#   기준으로 작성된 html 경로의 파일을 찾아오고
#   찾은 html을 렌더링(python 코드 해석 + str 변환) 후
#   HttpResponse에 담아서 반환
def index(request):
    return render(request, 'second/index.html')

def hello(request):
    return render(request, 'second/hello.html')