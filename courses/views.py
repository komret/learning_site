from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from . import models, forms


def course_list(request):
    courses = models.Course.objects.filter(
        published=True
    ).annotate(total_steps=Count('text', distinct=True) + Count('quiz', distincts=True))
    total = courses.aggregate(total=Sum('total_steps'))
    email = "komret@gmail.com"
    return render(request, "courses/course_list.html", {"courses": courses, "email": email, "total": total})


def course_detail(request, pk):
    try:
        course = models.Course.objects.prefetch_related(
            'quiz_set', 'text_set', 'quiz_set__question_set'
        ).get(pk=pk, published=True)
    except models.Course.DoesNotExist:
        raise Http404
    else:
        steps = sorted(chain(course.text_set.all(), course.quiz_set.all()), key=lambda step: step.order)
        return render(request, "courses/course_detail.html", {"course": course, "steps": steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk, course__published=True)
    return render(request, "courses/text_detail.html", {"step": step})


def quiz_detail(request, course_pk, step_pk):
    try:
        step = models.Quiz.objects.select_related('course').prefetch_related(
            'question_set', 'question_set__answer_set').get(course_id=course_pk, pk=step_pk, course__published=True)
    except models.Quiz.DoesNotExist:
        raise Http404
    else:
        return render(request, "courses/quiz_detail.html", {"step": step})


@login_required()
def create_quiz(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk, course__published=True)
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
    course = get_object_or_404(models.Course, pk=course_pk, course__published=True)
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
        form_class = forms.MultipleChoiceQuestionForm
    else:
        form_class = forms.TrueFalseQuestionForm

    form = form_class()
    answer_forms = forms.AnswerInlineFormSet(queryset=form.instance.answer_set.none())

    if request.method == "POST":
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormSet(request.POST, queryset=form.instance.answer_set.none())
        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)

            for answer in answers:
                answer.question = question
                answer.save()

            messages.success(request, "Question added!")
            return redirect(quiz.get_absolute_url())
    return render(request, "courses/question_form.html", {"quiz": quiz, "form": form, "formset": answer_forms})


@login_required()
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk, quiz_id=quiz_pk)

    if hasattr(question, "multiplechoicequestion"):
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion
    else:
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion

    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(queryset=form.instance.answer_set.all())

    if request.method == "POST":
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormSet(request.POST, queryset=form.instance.answer_set.all())
        if form.is_valid() and answer_forms.is_valid():
            question.save()
            answers = answer_forms.save(commit=False)

            for answer in answers:
                answer.question = question
                answer.save()

            for delete_item in answer_forms.deleted_objects:
                delete_item.delete()

            messages.success(request, "Question updated!")
            return redirect(question.quiz.get_absolute_url())
    return render(request, "courses/question_form.html", {"quiz": question.quiz, "form": form, "formset": answer_forms})


def courses_by_teacher(request, teacher):
    courses = models.Course.objects.filter(teacher__username=teacher, published=True)
    return render(request, "courses/course_list.html", {"courses": courses})


def search(request):
    term = request.GET.get("q")
    courses = models.Course.objects.filter(Q(title__icontains=term) | Q(description__icontains=term), published=True)
    return render(request, "courses/course_list.html", {"courses": courses})
