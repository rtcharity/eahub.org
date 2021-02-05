from django import forms


class ReportAbuseForm(forms.Form):
    CHOICES = [
        ("Spam", "Spam"),
        ("Fake account", "Fake account"),
        ("Offensive content", "Offensive content"),
    ]
    reasons = forms.MultipleChoiceField(
        choices=CHOICES, widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        cleaned_data = super(ReportAbuseForm, self).clean()
        if not cleaned_data["reasons"]:
            self._errors["reasons"] = [
                cleaned_data["reasons"]
            ]  # Will raise a error message
        else:
            return cleaned_data["reasons"]


class SendMessageForm(forms.Form):
    your_name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput)
    your_email_address = forms.CharField(
        label="Email", max_length=254, widget=forms.EmailInput
    )
    your_message = forms.CharField(
        label="Message", max_length=10000, widget=forms.Textarea
    )
