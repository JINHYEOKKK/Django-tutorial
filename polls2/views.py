from django.core.exceptions import ImproperlyConfigured
from django.db.models import F, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls2/index.html"
    context_object_name = "latest_question_list"
    ordering = '-pub_date'
    model = Question
    allow_empty = False

    def get(self, request, *args, **kwargs):
        # self.object_list 를 선언함으로써  인스턴스 변수로 저장하기 위함. 즉 클래스내 다른 메서드에서도 공유를 할 수 있음.
        # get_queryset() 의 리턴타입은 QuerySet
        self.object_list = self.get_queryset()
        print(type(self.object_list))
        # allow_empty 설정을 view.py에서 속성을 안줬다면 기본값은 MultipleObjectMixin에서 True 로 반환
        # get_allow_empty()의 리턴타입은 Boolean
        allow_empty = self.get_allow_empty()

        # 만약 view.py View 클래스 선언할때 allow_empty = False 속성을 준게 아니라면 이 조건문은 실행되지 않음
        if not allow_empty:
            # allow_empty가 False 라면 get_paginate_by함수로 object_list에 paginate_by속성을 가져와서 None이 아닌지 확인 및
            # hasattr() 함수로 object_list가 QuerySet 객체인지 특정속성'exists'이 객체에 존재하는지로 확인
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"):
                # 위 조건이 True 라면 object_list에 데이터가 존재하는지 QuerySet객체의 exists() 함수로 확인
                # 변수명이 is_empty 기 때문에 not 키워드를 사용해서 리턴값을 뒤집음. 데이터가 있으면 False로, 없으면 True로
                is_empty = not self.object_list.exists()
            else:
                # 리스트 타입은 exists() 함수가 없기 때문에 그냥 확인(파이썬에서 빈 값은 False임)
                is_empty = not self.object_list
            # if is_empty: 이 조건문은 is_empty가 True면 실행됨.
            # raise 는 파이썬에서 강제로 예외를 발생시키는 키워드. raise 예외클래스("에러 메시지")
            # _("텍스트") --> Django의 다국어 번역 함수(gettext)
            # %(class_name)s 는 문자열 포멧팅을 위한 변수 삽입 방식.
            # "class_name": self.__class__.__name__ 으로 "class_name" 에 현재 클래스의 이름을 할담함. (self.__class__.__name__는 현재 클래스의 이름을 가져옴)
            # 즉 실행 중인 클래스 이름을 자동으로 메시지에 포함 시킴.
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        # MultipleObjectMixin 를 부모로 상속받고 있기때문에 self. 키워드로 부모 메서드 get_context_data 사용
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        # object_list가 None 이 아니면 그 값을 사용. None 이면 self.object_list 사용 (즉, get_queryset()에서 가져온 데이터)
        queryset = object_list if object_list is not None else self.object_list
        # 가져온 데이터에서 view.py 에서 준 paginate_by 속성을 가져와 설정
        page_size = self.get_paginate_by(queryset)
        # 이것도 가져온 데이터에서 템플릿에서 사용할 context_object_name 속성 가져와 설정
        context_object_name = self.get_context_object_name(queryset)
        # 만약 page_size 에 값이 존재하면 True 이므로 페이지네이션을 적용
        # paginate_queryset(queryset, page_size) 을 호출하여 페이징 처리
        # paginator, page_obj, is_paginated, queryset을 context에 저장
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size
            )
            context = {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
            }
            # page_size 값 없으면 페이지네이션 적용 안한 속성들로 context에 저장
        else:
            context = {
                "paginator": None,
                "page_obj": None,
                "is_paginated": False,
                "object_list": queryset,
            }
        # context_object_name 속성값이 설정된 경우 할당해줌.
        if context_object_name is not None:
            context[context_object_name] = queryset
        # kwargs에 추가 데이터가 전달되면 기존 context에 업데이트
        context.update(kwargs)
        # 마지막으로 부모 클래스의 추가적인 컨텍스트 데이터를 포함시킴.
        # 상위 클래스에서 정의한 기본 컨텍스트 데이터를 유지하면서 확장 가능
        return super().get_context_data(**context)


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


class ViewQuestionUpdateView(generic.UpdateView):
    model = Question
    template_name = "polls2/result.html"


def sum_n_numbers(*args):
    print(type(args))
    return sum(args)


print(sum_n_numbers(1, 2, 3, 4), "\n")


def sum_n_words(**kwargs):
    print(type(kwargs))
    print(kwargs)
    return sum(kwargs.values())


sum_n_words(a=1, b=2, c=3, d=4)


def comprehension():
    # 딕셔너리를 List 로
    data = {"name": "Jim", "age": 29, "hobby": "Golf"}
    keys = [k for k, v in data.items()]

    return print(keys)


comprehension()


# "CreateView",
#     "UpdateView",
    # "DeleteView",
