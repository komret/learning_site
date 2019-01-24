from django import forms

from . import models


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = ["title", "description", "order", "total_questions"]


class TrueFalseQuestion(forms.ModelForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = ["order", "prompt"]


class MultipleChoiceQuestion(forms.ModelForm):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = ["order", "prompt", "shuffle_answers"]


class Answer(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["order", "text", "correct"]
