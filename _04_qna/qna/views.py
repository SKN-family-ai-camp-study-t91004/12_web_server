from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import AnswerForm, QuestionForm
from .models import Answer, Question

# @require_GET : HTTP Method = GET 유청만 처리
# @require_POST : HTTP Method = POST 유청만 처리

@require_GET
def index(request):
    query = request.GET.get('query', '').strip()
    questions = question_queryset()
    if query:
        questions = questions.filter(Q(subject__icontains=query) | Q(content__icontains=query))
    # Page는 현재 쪽의 질문과 전체 페이지 수를 함께 제공한다. 잘못된 page 값도 get_page가 보정한다.
    page_obj = Paginator(questions, 3).get_page(request.GET.get('page'))
    return render(request, 'qna/question_list.html', {'page_obj': page_obj, 'query': query})


@require_GET
def question_detail(request, id):
    question = get_object_or_404(detail_queryset(), pk=id)
    return render(request, 'qna/question_detail.html', {'question': question, 'answer_form': AnswerForm()})


@login_required(login_url='uauth:login')
@require_http_methods(['GET', 'POST'])
def question_create(request):
    form = QuestionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():

        # form 내부 model을 이용해서 전달 받은 데이터를 DB에 INSERT
        question = form.save(commit=False)
        question.author = request.user

        # 앞서 insert한 행에 author(사용자 pk)를 update, commit 기본값 True
        question.save()
        return redirect('qna:question_detail', id=question.pk)
    return render(request, 'qna/question_form.html', {'form': form})

def question_queryset():
    # 작성자는 JOIN, 여러 답변은 별도 조회로 가져와 목록의 N+1을 줄인다.
    return Question.objects.select_related('author').prefetch_related('answers').order_by('-created_at', '-pk')


def detail_queryset():
    # 답변의 작성자와 추천자도 미리 읽어 템플릿 순회 중 추가 SQL을 줄인다.
    answers = Answer.objects.select_related('author').prefetch_related('voters').order_by('created_at', 'pk')
    return Question.objects.select_related('author').prefetch_related('voters', Prefetch('answers', queryset=answers))


def check_owner(user, obj):
    # 질문·답변 모두 작성자 또는 staff만 수정·삭제한다. 화면 버튼과 별도로 검사한다.
    if obj.author_id != user.pk and not user.is_staff:
        raise PermissionDenied('작성자 또는 관리자만 변경할 수 있다.')


@login_required(login_url='uauth:login')
@require_http_methods(['GET', 'POST'])
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    check_owner(request.user, question)
    # instance가 기존 객체를 연결하므로 새 행 대신 해당 행을 수정한다.
    form = QuestionForm(request.POST if request.method == 'POST' else None, instance=question)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '정상적으로 수정되었습니다.')
        return redirect('qna:question_detail', id=question.pk)
    return render(request, 'qna/question_form.html', {'form': form})


@login_required(login_url='uauth:login')
@require_POST
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    check_owner(request.user, question)
    question.delete()
    messages.success(request, '정상적으로 삭제되었습니다.')
    return redirect('qna:index')

def invalid_answer(request, question_id, form):
    # 오류가 있는 폼을 다시 전달하여 빈 답변을 저장하지 않고 입력 오류를 표시한다.
    question = get_object_or_404(detail_queryset(), pk=question_id)
    return render(request, 'qna/question_detail.html', {'question': question, 'answer_form': form}, status=400)


@login_required(login_url='uauth:login')
@require_POST
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(request.POST)
    # 검증에 실패한 bound form에는 입력값과 오류가 남아 있어 상세 화면에서 다시 표시할 수 있다.
    if not form.is_valid():
        return invalid_answer(request, question.pk, form)
    answer = form.save(commit=False)
    answer.question, answer.author = question, request.user
    answer.save()
    return redirect(f'{resolve_url("qna:question_detail", id=question.pk)}#answer_{answer.pk}')


@login_required(login_url='uauth:login')
@require_POST
def answer_delete(request, id):
    answer = get_object_or_404(Answer, pk=id)
    check_owner(request.user, answer)
    # 돌아갈 질문은 조작 가능한 query string 대신 DB의 관계에서 얻는다.
    question_id = answer.question_id
    answer.delete()
    return redirect('qna:question_detail', id=question_id)


@login_required(login_url='uauth:login')
@require_POST
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    check_owner(request.user, answer)
    # 같은 답변을 instance로 연결하여 검증된 content만 바꾼다. 작성자와 질문 관계는 유지한다.
    # auto_id는 입력 name을 유지하고 신규 등록 폼과 HTML id만 구분한다.
    form = AnswerForm(request.POST, instance=answer, auto_id='answer_modify_%s')
    if not form.is_valid():
        # 수정 오류는 해당 답변의 수정 폼으로 돌리고 신규 등록 폼은 비워 둔다.
        question = get_object_or_404(detail_queryset(), pk=answer.question_id)
        return render(request, 'qna/question_detail.html', {
            'question': question,
            'answer_form': AnswerForm(),
            'answer_modify_form': form,
            'answer_modify_id': answer.pk,
        }, status=400)
    form.save()
    return redirect(f'{resolve_url("qna:question_detail", id=answer.question_id)}#answer_{answer.pk}')

def toggle_vote(obj, user):
    # 사용자당 관계 하나를 추가하거나 제거한다. 다시 추천하면 취소한다.
    if obj.voters.filter(pk=user.pk).exists():
        obj.voters.remove(user)
    else:
        obj.voters.add(user)


@login_required(login_url='uauth:login')
@require_POST
def question_vote(request, id):
    question = get_object_or_404(Question, pk=id)
    toggle_vote(question, request.user)
    # HTML 대신 JSON을 응답한다. 브라우저 fetch가 vote_count로 추천 수만 바꾼다.
    return JsonResponse({'result': 'success', 'question_id': question.pk, 'vote_count': question.voters.count()})


@login_required(login_url='uauth:login')
@require_POST
def answer_vote(request, id):
    answer = get_object_or_404(Answer, pk=id)
    toggle_vote(answer, request.user)
    return JsonResponse({'result': 'success', 'answer_id': answer.pk, 'vote_count': answer.voters.count()})

@require_GET
def question_search(request):
    query = request.GET.get('query', '').strip()
    questions = Question.objects.filter(Q(subject__icontains=query) | Q(content__icontains=query)).order_by('-created_at', '-pk')[:20] if query else []
    return JsonResponse({'results': [{'id': q.pk, 'text': q.subject} for q in questions]})