from django.urls import path, re_path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("<int:pk>/", views.course_detail, name="detail"),
    path("<int:course_pk>/t<int:step_pk>/", views.text_detail, name="text"),
    path("<int:course_pk>/q<int:step_pk>/", views.quiz_detail, name="quiz"),
    path("<int:course_pk>/create_quiz/", views.create_quiz, name="create_quiz"),
    path("<int:course_pk>/edit_quiz/<int:quiz_pk>", views.edit_quiz, name="edit_quiz"),
    re_path(
        r"(?P<quiz_pk>\d+)/create_question/(?P<question_type>mc|tf)/$",
        views.create_question,
        name="create_question"
    ),
    path("<int:quiz_pk>/edit_question/<int:question_pk>", views.edit_question, name="edit_question"),
]
