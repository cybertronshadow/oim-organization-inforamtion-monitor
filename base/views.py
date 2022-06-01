from datetime import datetime
from unicodedata import category
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .decorators import *

from .models import *
from .forms import *
import csv


def registrationge(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

        else:
            messages.error(request, "There was an error in registration")
            return redirect('home-page')
    context = {'form': form}
    return render(request, 'signup.html', context)


@unauthenticated_user
def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "Wrong Username or Password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "Wrong username or Password")

    context = {}
    return render(request, 'login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login-page')


@login_required(login_url='login-page')
def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    employees = Employees.objects.all()
    departments = Department.objects.all()
    annoucement_messages = Messages.objects.all()
    annoucements = Annoucements.objects.filter(
        Q(department__body__icontains=q) |
        Q(host__username__icontains=q) |
        Q(title__icontains=q)
    )

    context = {'employees': employees,
               'departments': departments, 'annoucements': annoucements, 'annoucement_messages': annoucement_messages}
    return render(request, 'home.html', context)


@login_required(login_url='login-page')
def employeespage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    annoucements = Annoucements.objects.all()
    leave = Dayend.objects.all()

    employees = Employees.objects.filter(
        Q(department__body__icontains=q) |
        Q(user__username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(second_name__icontains=q)
    )
    departments = Department.objects.all()
    context = {'employees': employees,
               'departments': departments, 'annoucements': annoucements, 'leave': leave}
    return render(request, 'employees.html', context)


@login_required(login_url='login-page')
def annoucementpage(request, pk):
    employee = Employees.objects.all()
    annoucement = Annoucements.objects.get(id=pk)
    annoucement_messages = annoucement.messages_set.all()
    participants = annoucement.participants.all()
    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,

            annoucement=annoucement,
            body=request.POST.get('body')
        )
        annoucement.participants.add(request.user)
        return redirect('annoucement-page', pk=annoucement.id)

    context = {'annoucement': annoucement,
               'annoucement_messages': annoucement_messages, 'participants': participants}
    return render(request, 'annoucement.html', context)


@login_required(login_url='login-page')
def newannoucement(request):
    form = AnnoucementForm()

    if request.method == 'POST':
        form = AnnoucementForm(request.POST)
        if form.is_valid():
            annoucement = form.save(commit=False)
            annoucement.host = request.user
            annoucement.save()
            return redirect('home-page')
    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def updateannoucement(request, pk):
    annoucement = Annoucements.objects.get(id=pk)
    form = AnnoucementForm(instance=annoucement)

    if request.user != annoucement.host:
        return HttpResponse('Not allowed here')

    if request.method == 'POST':
        form = AnnoucementForm(request.POST, instance=annoucement)
        if form.is_valid():
            form.save()
            return redirect('home-page')

    context = {'annoucement': annoucement, 'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def deleteannoucement(request, pk):
    item = Annoucements.objects.get(id=pk)

    if request.user != item.host:
        return HttpResponse('Not allowed here')
    if request.method == 'POST':
        item.delete()
        return redirect('home-page')

    context = {'item': item}
    return render(request, 'delete.html', context)


@login_required(login_url='login-page')
def checkinemployee(request):
    form = EmployeesForm()

    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('employees-page')
    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def updateemployee(request, pk):
    employee = Employees.objects.get(id=pk)
    form = EmployeesForm(instance=employee)
    if request.user != employee.user:
        return HttpResponse('Not allowed here')
    if request.method == 'POST':
        form = EmployeesForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees-page')

    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def assetspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()
    assets = Assests.objects.filter(
        Q(category__body__icontains=q) |
        Q(user__username__icontains=q) |
        Q(name__icontains=q)

    )

    context = {'assets': assets, 'categories': categories}
    return render(request, 'assets.html', context)


@login_required(login_url='login-page')
@allowed_users(allowed_roles=['admin', 'hod'])
def newasset(request):
    form = AssetForm()
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            return redirect('assets-page')
    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def updateasset(request, pk):
    asset = Assests.objects.get(id=pk)
    form = AssetForm(instance=asset)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('assets-page')

    context = {'form': form}
    return render(request, 'new_item.html', context)


def deleteasset(request, pk):
    asset = Assests.objects.get(id=pk)
    if request.method == 'POST':
        asset.delete()
        return redirect('assets-page')
    context = {'item': asset}
    return render(request, 'delete.html', context)


@login_required(login_url='login-page')
def faqspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    departments = Department.objects.all()
    faqs = Faq.objects.filter(
        Q(title__icontains=q) |
        Q(department__body__icontains=q) |
        Q(description__icontains=q)
    )
    context = {'faqs': faqs, 'departments': departments}
    return render(request, 'faqs.html', context)


@login_required(login_url='login-page')
def faqpage(request, pk):
    faq = Faq.objects.get(id=pk)
    context = {'faq': faq}
    return render(request, 'faq.html', context)


@login_required(login_url='login-page')
def createfaq(request):
    form = FaqForm()
    if request.method == "POST":
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.user = request.user
            faq.save()
            return redirect('faqs-page')

    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def updatefaq(request, pk):
    faq = Faq.objects.get(id=pk)
    form = FaqForm(instance=faq)
    if request.method == 'POST':
        form = FaqForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faqs-page')
    context = {'form': form}
    return render(request, 'new_item.html', context)


@login_required(login_url='login-page')
def deletefaq(request, pk):
    faq = Faq.objects.get(id=pk)
    if request.method == 'POST':
        faq.delete()
        return redirect('faqs-page')

    context = {'item': faq}
    return render(request, 'delete.html', context)


@login_required(login_url='login-page')
def exportcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=Employees' + \
        str(datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'second_name',
                    'last_name', 'employee_id', 'designination', 'phone_number', 'department', 'Date'])

    employees = Employees.objects.all()

    for employee in employees:
        writer.writerow([employee.first_name, employee.second_name, employee.last_name, employee.employee_id,
                        employee.designination, employee.phone_number, employee.department, employee.created])

    return response


@login_required(login_url='login-page')
def exportassets(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=Assets' + \
        str(datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['name', 'serial_no', 'department',
                    'employee', 'category', 'Date'])

    assets = Assests.objects.all()

    for asset in assets:
        writer.writerow([asset.name, asset.serial_no, asset.department, asset.employee,
                        asset.category, asset.created])

    return response


@login_required(login_url='login-page')
def deletemessage(request, pk):
    annoucement_message = Messages.objects.get(id=pk)
    if request.method == 'POST':
        annoucement_message.delete()
        return redirect('home-page')

    context = {'item': annoucement_message}
    return render(request, 'delete.html', context)


@login_required(login_url='login-page')
def checkout(request, pk):
    employee = Employees.objects.get(id=pk)

    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            dayend = form.save(commit=False)
            dayend.user = request.user
            dayend.save()
            return redirect('employees-page')

    context = {'employee': employee, 'form': form}
    return render(request, 'checkout.html', context)


@login_required(login_url='login-page')
def userpage(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'users.html', context)


@login_required(login_url='login-page')
def profilepage(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context)
