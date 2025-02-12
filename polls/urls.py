from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),

    path("<int:question_id>/", views.detail, name="detail"),

    # ex: /polls/5/results/
    path("<int:question_id>/result/", views.results, name="result"),

    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # ---------------------------------------- Test
    path("index", views.question_list, name="question_list"),
    path("<int:pk>/", views.question_detail, name="question_detail")

]