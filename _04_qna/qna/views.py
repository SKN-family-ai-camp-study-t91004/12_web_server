from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from .forms import QuestionForm
from .models import Question

# @require_GET : HTTP Method = GET 유청만 처리
# @require_POST : HTTP Method = POST 유청만 처리

@require_GET
def index(request):
    questions = Question.objects.select_related('author').order_by('-created_at', '-pk')
    return render(request, 'qna/question_list.html', {'questions': questions})


@require_GET
def question_detail(request, id):
    question = get_object_or_404(Question.objects.select_related('author'), pk=id)
    return render(request, 'qna/question_detail.html', {'question': question})


@login_required(login_url='uauth:login')
@require_http_methods(['GET', 'POST'])
def question_create(request):
    form = QuestionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        question.author = request.user
        question.save()
        return redirect('qna:question_detail', id=question.pk)
    return render(request, 'qna/question_form.html', {'form': form})