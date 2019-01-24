from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from . import models


def course_list(request):
    courses = models.Course.objects.all()
    email = "komret@gmail.com"
    return render(request, "courses/course_list.html", {"courses": courses, "email": email})


def course_detail(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    steps = sorted(chain(course.text_set.all(), course.quiz_set.all()), key=lambda step: step.order)
    return render(request, "courses/course_detail.html", {"course": course, "steps": steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, "courses/text_detail.html", {"step": step})


def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz, course_id=course_pk, pk=step_pk)
    return render(request, "courses/quiz_detail.html", {"step": step})


@login_required()
def create_quiz(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()
    if request.method == "POST":
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, "Quiz added!")
            return redirect(quiz.get_absolute_url())
    return render(request, "courses/quiz_form.html", {"course": course, "form": form})


@login_required()
def edit_quiz(request, course_pk, quiz_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk)
    form = forms.QuizForm(instance=quiz)
    if request.method == "POST":
        form = forms.QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {form.cleaned_data['title']}.")
            return redirect(quiz.get_absolute_url())
    return render(request, "courses/quiz_form.html", {"course": course, "form": form})


@login_required()
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)

    if question_type == "mc":
        form_class = forms.MultipleChoiceQuestion
    else:
        form_class = forms.TrueFalseQuestion

    form = form_class()

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question added!")
            return redirect(quiz.get_absolute_url())
    return render(request, "courses/question_form.html", {"quiz": quiz, "form": form})


@login_required()
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk, quiz_id=quiz_pk)

    if hasattr(question, "multiplechoicequestion"):
        form_class = forms.MultipleChoiceQuestion
        question = question.multiplechoicequestion
    else:
        form_class = forms.TrueFalseQuestion
        question = question.truefalsequestion

    form = form_class(instance=question)

    if request.method == "POST":
        form = form_class(request.POST, instance=question)
        if form.is_valid():
            question.save()
            messages.success(request, "Question updated!")
            return redirect(question.quiz.get_absolute_url())
    return render(request, "courses/question_form.html", {"quiz": question.quiz, "form": form})


@login_required()
def create_answer(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)
    form = forms.Answer()

    if request.method == "POST":
        form = forms.Answer(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, "Answer Added!")
            return redirect(question.quiz.get_absolute_url())
    return render(request, "courses/answer_form.html", {"question": question, "form": form})
