from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls2/index.html"
    context_object_name = "latest_question_list"
    ordering = '-pub_date'
    model = Question

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by("-pub_date")[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = "polls2/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls2/result.html"


def vote(request, question_id):
    # get_object_or_404() 내장함수는 히나의 툭정 객체를 가져오거나, 존재하지 않을 결우 자동으로 404 오류메시지를 발생시킴
    # 파라미터로는 모델 클래스, 모델 매니저, QuerySet 중 하나
    # 다수의 객체를 가져오려면 get_list_or_404()
    # hasattr(객체, "속성 는 메서드") <-- 객체가 속성이나, 메서드를 가지고 있으면 True
    # klass 는 Class, Manager, QuerySet 중 하나를 받을 수 있는 변수. --> 왜 class 가 아니고 klass 인 이유는 class 는 파이썬에서 예약어이기 때문임
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls2/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # F() 객체는 데이터베이스 내에서 필드 값을 직접 수정하고, 이 수정된 값을 데이터베이스에 반영하도록 돕는 역할.
        # 예를 예를 들어, F("votes") + 1은 현재 votes 필드 값에 1을 더하는 연산을 데이터베이스에서 바로 수행하도록 함.
        # F("votes")는 데이터베이스 내 votes 필드의 현재 값을 의미. + 1은 그 값을 1 증가시키는 연산을 함.
        # 이 코드는 votes 필드에 대한 값을 메모리에서 처리하는 것이 아니라, db에서 직접 현재 votes 값에 1을 더해서 업데이트하는 방식. 이유는 동시성 문제.
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls2:results", args=(question.id,)))
        # return redirect("polls2:results", pk=question.id)


