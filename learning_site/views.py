from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from . import forms


def hello_world(request):
    return render(request, "home.html")


def suggestion(request):
    form = forms.SuggestionForm()
    if request.method == 'POST':
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                f"Suggestion from {form.cleaned_data['name']}",
                form.cleaned_data['suggestion'],
                f"{form.cleaned_data['name']} <{form.cleaned_data['email']}>",
                ["komret@gmail.com"]
            )
            messages.add_message(request, messages.SUCCESS,
                                 'Thanks for your suggestion!')
            return redirect('suggestion')
    return render(request, 'suggestion_form.html', {'form': form})
