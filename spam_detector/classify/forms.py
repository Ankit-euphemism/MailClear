from django import forms

class EmailForm(forms.Form):
    email_text = forms.CharField(
        label='Paste your email here',
        max_length=10000,
        widget=forms.Textarea(
            attrs={
                'rows': 12,
                'placeholder': 'Paste the full email content here (subject + body) for better accuracy...',
                'class': 'email-input',
                'autocomplete': 'off',
            }
        ),
    )