from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Course, Usermember, Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def homepage(request):
    return render(request, "homepage.html")

def registerpage(request):
    return render(request, "registerpage.html")

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']
        age = request.POST['age']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        photo = request.FILES['photo']
        course_name = request.POST['course']

        if password != confirm_password:
            return render(request, 'registerpage.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        course, created = Course.objects.get_or_create(course_name=course_name, defaults={'fee': 0}) 

        user_member = Usermember.objects.create(
            user=user,
            course=course,
            address=address,
            age=age,
            number=contact_number,
            image=photo
        )

        # Log in the user
        login(request, user)

        success_message = 'Successfully registered!'
        return render(request, 'registerpage.html', {'success_message': success_message})
    
    return render(request, 'registerpage.html')


def loginpage(request):
    return render(request, "loginpage.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            
            if username == 'admin' and password == 'admin':
                return redirect('adminprofile')
            else:
                return redirect('userprofile')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'loginpage.html')

def userprofile(request):
    user_member = Usermember.objects.get(user=request.user)
    return render(request, 'userprofile.html', {'user_member': user_member})

def updateprofile(request):
    user_member = Usermember.objects.get(user=request.user)
    return render(request, 'updateprofile.html', {'user_member': user_member})

def update_user(request):
    if request.method == 'POST':
        user_member = Usermember.objects.get(user=request.user)

        user_member.user.first_name = request.POST['first_name']
        user_member.user.last_name = request.POST['last_name']
        user_member.user.email = request.POST['email']
        user_member.address = request.POST['address']
        user_member.age = request.POST['age']
        user_member.number = request.POST['contact_number']
        user_member.course.course_name = request.POST['course']

        if 'photo' in request.FILES:
            user_member.image = request.FILES['photo']

        user_member.user.save()
        user_member.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('userprofile')

    user_member = Usermember.objects.get(user=request.user)
    return render(request, 'updateprofile.html', {'user_member': user_member})


def logout_user(request):
    return redirect('homepage')

def adminprofile(request):
    return render(request, 'adminprofile.html')

def add_course_page(request):
    return render(request, 'add_course_page.html')

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name') 
        fee = request.POST.get('course_fees') 
        course = Course(course_name=course_name, fee=fee)
        course.save()
        return redirect('add_course_page')

def add_student_page(request):
    courses = Course.objects.all()
    return render(request, "add_student_page.html", {'courses': courses})

def add_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('student_address')
        age = request.POST.get('student_age')
        joining_date = request.POST.get('joining_date')
        course_id = request.POST.get('course_name')
        course = Course.objects.get(pk=course_id)
        student = Student(name=name, student_address=address, student_age=age, joining_date=joining_date, course=course)
        student.save()
        return redirect('view_student_page')

    courses = Course.objects.all()
    return render(request, 'add_student_page.html', {'courses': courses})

def view_student_page(request):
    students = Student.objects.select_related('course').all()
    return render(request, "view_student_page.html", {'students': students})

def student_update_page(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    courses = Course.objects.all()
    return render(request, "student_update_page.html", {'student': student, 'courses': courses})

def student_update(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        student.name = request.POST.get('name')
        student.student_address = request.POST.get('student_address')
        student.student_age = request.POST.get('student_age')
        student.joining_date = request.POST.get('joining_date')
        course_id = request.POST.get('course_name')
        student.course = Course.objects.get(pk=course_id)
        student.save()
        return redirect('view_student_page')

    courses = Course.objects.all()
    return render(request, 'student_update_page.html', {'student': student, 'courses': courses})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('view_student_page')

    return render(request, 'confirm_delete_student.html', {'student': student})

def view_teacher_page(request):
    teachers = Usermember.objects.all()
    return render(request, 'view_teacher_page.html', {'teachers': teachers})

def delete_teacher(request, teacher_id):
    teacher = Usermember.objects.get(id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('view_teacher_page')
    return render(request, 'confirm_delete_teacher.html', {'teacher': teacher})

def logout_admin(request):
    return redirect('homepage')


