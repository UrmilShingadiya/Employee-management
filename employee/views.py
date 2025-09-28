from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from .forms import CustomUserCreationForm, LetterForm, EmployeeForm, ContactForm
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required

@require_POST
def toggle_employee_status(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = not employee.is_active
    employee.save()
    return redirect('all_employees')

def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # You could send an email here or save it to the database
            messages.success(request, "Thank you for contacting us. We'll get back to you soon.")
            return redirect('contact')  # Assuming 'contact' is the name in urls.py
    return render(request, 'contact_us.html', {'form': form})
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_employees')
    else:
        form = EmployeeForm()
    return render(request, 'employee/add_employee.html', {'form': form})
@login_required
def all_employees(request):
    employees = Employee.objects.all()
    return render(request, 'employee/all_employees.html', {'employees': employees})
@login_required 
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/employee_detail.html', {'employee': employee})

@login_required
def dashboard(request):
    today = date.today()
    three_days_later = today + timedelta(days=3)

    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    expired_contracts = Employee.objects.filter(end_date__lt=today).count()
    recent_joins = Employee.objects.filter(date_of_joining__month=today.month).count()

    expiring_contracts = Employee.objects.filter(
        end_date__range=(today, three_days_later),
        is_active=True
    )

    recent_employees = Employee.objects.order_by('-id')[:5]  # last 5 added

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'expired_contracts': expired_contracts,
        'recent_joins': recent_joins,
        'expiring_contracts': expiring_contracts,
        'recent_employees': recent_employees,
    }

    return render(request, 'dashboard.html', context)
@login_required
def home(request):

    today = date.today()
    warning_date = today + timedelta(days=3)

    # Employees whose contract ends in the next 3 days
    expiring_contracts = Employee.objects.filter(
        end_date__isnull=False,
        end_date__range=(today, warning_date),
        is_active=True
    )
    employees = Employee.objects.all()
    return render(request, 'home.html', {
            'employees': employees,
            'expiring_contracts': expiring_contracts})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact_us.html')

def profile_view(request):
    return render(request, 'profile.html')  # Create profile.html later


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged in users

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Send welcome email
            subject = 'Welcome to Our Blog!'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            html_message = render_to_string('emails/welcome_email.html', {'username': user.username})
            plain_message = f"Hi {user.username},\n\nWelcome to our blog!"

            email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
            email.attach_alternative(html_message, "text/html")
            email.send()

            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def generate_offer_letter(request):
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            html = render_to_string('letters/offer_letter.html', context)

            # Create a PDF response
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'

            # Generate PDF
            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                return HttpResponse('We had some errors while generating the PDF.')

            return response
        else:
            # ❗ If form is invalid, return the form with errors
            return render(request, 'letters/letter_form.html', {'form': form, 'title': 'Generate Offer Letter'})
    
    else:
        form = LetterForm()
        return render(request, 'letters/letter_form.html', {'form': form, 'title': 'Generate Offer Letter'})

@login_required
def generate_joining_letter(request):
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            html = render_to_string('letters/joining_letter.html', context)
            return HttpResponse(html)
    else:
        form = LetterForm()
    return render(request, 'letters/letter_form.html', {'form': form, 'title': 'Generate Joining Letter'})
