from django.shortcuts import render, redirect
from .forms import ApplicationForm
from programs.models import Program
from .models import Application
from django.contrib.auth.decorators import login_required

def apply(request):
    program_id = request.GET.get('program')
    initial_data = {}

    if program_id:
        initial_data['program'] = Program.objects.get(id=program_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'admissions/success.html')
    else:
        form = ApplicationForm(initial=initial_data)

    return render(request, 'admissions/apply.html', {'form': form})
@login_required
def apply_program(request, program_id):
    student = request.user.profile
    program = Program.objects.get(id=program_id)

    Application.objects.create(
        student=student,
        program=program
    )

    return redirect('student_dashboard')

