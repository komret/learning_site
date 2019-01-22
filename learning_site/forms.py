from django import forms


def must_be_empty(value):
    if value:
        raise forms.ValidationError("is not empty.")


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField()
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="Leave empty",
        validators=[must_be_empty]
    )

    def clean(self):
        if super().clean()["email"] != super().clean()["verify_email"]:
            raise forms.ValidationError("The emails must match!")
