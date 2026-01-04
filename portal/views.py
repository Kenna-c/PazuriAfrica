from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accademics.models import Module, Result, Fee, Lecture, Assignment, AssignmentSubmission, Attendance
from accounts.models import Student
#from programs.models import Module
from .decorators import staff_required, student_required
#from programs.models import ProgramApplication
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout as auth_logout
from admissions.models import Application


@never_cache
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'student':
        return redirect('student_dashboard')
    elif profile.role == 'staff':
        return redirect('staff_dashboard')
    else:
        return redirect('/admin/')

# @login_required
# def student_dashboard(request):
#     return render(request, 'portal/student_dashboard.html')

# @login_required
# def staff_dashboard(request):
#     return render(request, 'portal/staff_dashboard.html')

@never_cache
@login_required
def student_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    student = Student.objects.filter(profile=profile).first()
    if not student:
        return render(request, 'portal/no_student_record.html')

    application = student.application
    if application:
        modules = Module.objects.filter(programs=application.program)
    else:
        modules = Module.objects.none()

    results = Result.objects.filter(student=student.profile)
    attendance_records = Attendance.objects.filter(
        student=student.profile,
        module__in=modules
    )
    assignments = Assignment.objects.filter(module__in=modules)
    fees = Fee.objects.filter(student=student.profile)
    context = {
        'profile': profile,
        'application': application,
        'modules': modules,
        'results': results,
        'attendance_records': attendance_records,
        'assignments': assignments,
        'fees': fees,
    }

    return render(request, 'portal/student_dashboard.html', context)


@never_cache
@login_required
@staff_required
def staff_dashboard(request):
    modules = Module.objects.filter(lecturer__user=request.user).prefetch_related('students')
    assignments = Assignment.objects.filter(module__in=modules)
    lectures = Lecture.objects.filter(module__in=modules)

    context = {
        'modules': modules,
        'assignments': assignments,
        'lectures': lectures,
    }
    # print(request.user.username)
    # print(request.user.is_superuser)
    # print(request.user.profile.role)

    return render(request, 'portal/staff_dashboard.html', context)

@never_cache
@login_required
@staff_required
def staff_module_detail(request, module_id):
    module = Module.objects.get(id=module_id, lecturer__user=request.user)
    # lectures = Lecture.objects.filter(module=module)
    # assignments = Assignment.objects.filter(module=module)
    student = module.students.all()

    context = {
        'module': module,
        'students': student,
    }
    return render(request, 'portal/staff_module_detail.html', context)

@never_cache
@login_required
@staff_required
def upload_results(request, module_id):
    module = Module.objects.get(id=module_id)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        grade = request.POST.get('grade')
        score = request.POST.get('score')

        student_profile = Profile.objects.get(id=student_id)
        Result.objects.create(student=student_profile, module=module, grade=grade, score=score)

        return redirect('staff_module_detail', module_id=module.id)

    students = Profile.objects.filter(role='student')
    context = {
        'module': module,
        'students': students,
    }
    return render(request, 'portal/upload_results.html', context)

@never_cache
@login_required
@student_required
def fee_payment(request):
    profile = request.user.profile
    fee = Fee.objects.get(student=profile)

    if request.method == 'POST':
        amount_paid = float(request.POST.get('amount_paid'))
        fee.amount_paid += amount_paid
        fee.balance = fee.total_fee - fee.amount_paid
        fee.save()

        return redirect('fee_balance')

    context = {
        'fee': fee
    }
    return render(request, 'portal/fee_payment.html', context)

@never_cache
@login_required
@student_required
def fee_history(request):
    profile = request.user.profile
    fee = Fee.objects.get(student=profile)
    payments = fee.payments.all()

    context = {
        'payments': payments
    }
    return render(request, 'portal/fee_history.html', context)

@never_cache
@login_required
@student_required
def fee_balace(request):
    profile = request.user.profile
    fee = Fee.objects.get(student=profile)

    context = {
        'fee': fee
    }
    return render(request, 'portal/fee_balance.html', context)

@never_cache
@login_required
@student_required
def view_lectures(request):
    profile = request.user.profile
    modules = Module.objects.filter(program=profile.program)
    lectures = Lecture.objects.filter(module__in=modules)

    context = {
        'lectures': lectures
    }
    return render(request, 'portal/view_lectures.html', context)

@never_cache
@login_required
@student_required
def view_assignments(request):
    profile = request.user.profile
    modules = Module.objects.filter(program=profile.program)
    assignments = Assignment.objects.filter(module__in=modules)

    context = {
        'assignments': assignments
    }
    return render(request, 'portal/view_assignments.html', context)
@login_required
@student_required
def logout(request):
    auth_logout(request)

    return redirect('login')

@never_cache
@login_required
@staff_required
def staff_lectures(request):
    profile = request.user.profile
    modules = Module.objects.filter(lecturer=profile)
    lectures = Lecture.objects.filter(module__in=modules)

    context = {
        'lectures': lectures
    }
    return render(request, 'portal/staff_lectures.html', context)
@never_cache
@login_required
@staff_required
def upload_results(request):
    profile = request.user.profile
    modules = Module.objects.filter(lecturer=profile)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        module_id = request.POST.get('module_id')
        grade = request.POST.get('grade')
        score = request.POST.get('score')

        student_profile = Profile.objects.get(id=student_id)
        module = Module.objects.get(id=module_id)
        Result.objects.create(student=student_profile, module=module, grade=grade, score=score)

        return redirect('staff_dashboard')

    students = Profile.objects.filter(role='student')
    context = {
        'modules': modules,
        'students': students,
        'module': module,
    }
    return render(request, 'portal/upload_results.html', context)

@never_cache
@login_required
@student_required
def student_attendance(request):
    profile = request.user.profile
    modules = Module.objects.filter(program=profile.program)
    attendance_records = Attendance.objects.filter(student=profile, module__in=modules)

    context = {
        'attendance_records': attendance_records
    }
    return render(request, 'portal/student_attendance.html', context)
@never_cache
@login_required
@staff_required
def staff_module_detail(request, module_id):
    module = Module.objects.get(id=module_id)
    lectures = Lecture.objects.filter(module=module)
    assignments = Assignment.objects.filter(module=module)

    context = {
        'module': module,
        'lectures': lectures,
        'assignments': assignments,
        'module': module,

    }
    return render(request, 'portal/staff_module_detail.html', context)