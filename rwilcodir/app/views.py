from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .models import Employee, Training, TrainingStatus
from .forms import HelpForm
from django.db.models import Q
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_supervisor:
                return redirect('supervisor')
            else:
                return redirect('current_training')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def current_training_view(request):
    try:
        employee_id = request.user.employee_id
        training_statuses = TrainingStatus.objects.filter(employee__employee_id=employee_id).select_related('training')
        completion_percentage = 100 * training_statuses.filter(completion_date__isnull=False).count() / training_statuses.count()
    except AttributeError:
        training_statuses = None
        completion_percentage = 0

    for training in training_statuses:
        if training.completion_date is not None:
            training.is_complete = True
        else:
            training.is_complete = False

    context = {
        'training_statuses': training_statuses,
        'completion_percentage': completion_percentage
    }

    return render(request, 'app/current_training.html', context)



@login_required
def training_search_view(request):
    trainings = None
    search_query = request.POST.get('search_query', '')
    if search_query:
        employee_id = request.user.employee_id
        trainings = Training.objects.filter(
            Q(name__icontains=search_query) |
            Q(trainingstatus__employee__employee_id=employee_id, training_id=search_query)
        )
    return render(request, 'training_search.html', {'trainings': trainings, 'search_query': search_query})


@login_required
def employee_search_view(request):
    employees = None
    search_query = request.GET.get('search', '')
    error_message = None

    if search_query:
        if search_query.isdigit():
            try:
                employees = Employee.objects.filter(employee_id=search_query)
            except Employee.DoesNotExist:
                employees = None
        else:
            error_message = "Invalid Input Detected. Search Only Using Employee ID Number."

    context = {
        'employees': employees,
        'search_query': search_query,
        'error_message': error_message
    }
    return render(request, 'employee_search.html', context)


@login_required
def supervisor_view(request):
    supervisor_id = request.user.employee_id
    employees = Employee.objects.filter(supervisor__employee_id=supervisor_id)
    employee_stats = []
    for employee in employees:
        trainings = TrainingStatus.objects.filter(employee=employee).prefetch_related('training')
        if trainings:
            percent_complete = sum([t.completion_date is not None for t in trainings])/len(trainings)*100
        else:
            percent_complete = 0
        employee_stats.append({
            'employee': employee,
            'percent_complete': percent_complete,
            'trainings': trainings
        })
    return render(request, 'supervisor.html', {'employee_stats': employee_stats})



def help_view(request):
    form = HelpForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        employee_id = form.cleaned_data['employee_id']
        description = form.cleaned_data['description']
        send_mail(
            'Help Request',
            f'Employee Name: {first_name} {last_name}\nEmployee ID: {employee_id}\nDescription: {description}',
            settings.EMAIL_HOST_USER,  # use the default email address as the from_email
            ['rogerwilcotech@gmail.com'],  # replace the recipient email with your desired email
            fail_silently=False,
        )
        messages.success(request, 'Help request submitted successfully.')
        return redirect('help')
    return render(request, 'help.html', {'form': form})
