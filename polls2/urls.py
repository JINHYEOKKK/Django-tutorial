from django.urls import path
from . import views

app_name = "polls2"

urlpatterns = [
    # ListView
    path("", views.IndexView.as_view(), name="index"),
    # DetailView
    path("<int:pk>", views.DetailView.as_view(), name="detail"),
    # name="resultes" <-- 를 polls2:results 로 참조 가능
    # pk 와 question_id 의 차이점
    # 클래스기반뷰(CBV) 에서는 기본적으로 pk모델의 기본키를 변수명으로 사용
    # 함수기반뷰(FBV) 에서는 pk를 사용해야하는 규칙이 없어서 자요롭게 설정가능
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
