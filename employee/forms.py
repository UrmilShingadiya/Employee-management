from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LetterForm(forms.Form):

    POSITION_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('HR Executive', 'HR Executive'),
        ('Marketing Manager', 'Marketing Manager'),
        ('Intern', 'Intern'),
    ]
     
    full_name = forms.CharField(label='Full Name', max_length=100)
    position = forms.ChoiceField(label='Position',choices=POSITION_CHOICES)
    start_date = forms.DateField(label='Start Date', widget=forms.SelectDateWidget)
    salary = forms.DecimalField(label='Salary', max_digits=10, decimal_places=2)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Type your message here...'}))
