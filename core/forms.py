from django import forms

class ContactForm(forms.Form):
    """
    Contact form for the contact page
    """
    DEPARTMENT_CHOICES = [
        ('general', 'General Inquiry'),
        ('membership', 'Membership'),
        ('events', 'Events'),
        ('scholarship', 'Scholarship Program'),
        ('partnership', 'Partnership'),
        ('feedback', 'Feedback/Suggestions'),
        ('other', 'Other'),
    ]
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject of your message',
        })
    )
    
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message...',
        })
    )
    
    def clean_message(self):
        """
        Validate the message field
        """
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Your message is too short. Please provide more details.")
        return message
