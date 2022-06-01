from unicodedata import name
from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginpage, name="login-page"),
    path('logout/', views.logoutuser, name="logout-page"),
    path('registration/', views.registrationge, name="registration-page"),


    path('', views.homepage, name="home-page"),
    path('employees/', views.employeespage, name="employees-page"),
    path('annoucement/<str:pk>/', views.annoucementpage, name="annoucement-page"),


    path('newannoucement/', views.newannoucement, name="new-annoucement"),
    path('updateannoucement/<str:pk>/',
         views.updateannoucement, name="update-annoucement"),
    path('delete/<str:pk>/', views.deleteannoucement, name="delete-annoucement"),

    path('checkin/', views.checkinemployee, name="employee-checkin"),
    path('updatedetails/<str:pk>/', views.updateemployee, name="update-employee"),

    path('assetspage/', views.assetspage, name="assets-page"),
    path('newasset/', views.newasset, name="new-asset"),
    path('updateasset/<str:pk>/', views.updateasset, name="update-asset"),
    path('deleteasset/<str:pk>/', views.deleteasset, name="delete-asset"),

    path('faqspage/', views.faqspage, name="faqs-page"),
    path('createfaq/', views.createfaq, name="create-faq"),
    path('updatefaq/<str:pk>/', views.updatefaq, name="update-faq"),
    path('deletefaq/<str:pk>/', views.deletefaq, name="delete-faq"),
    path('faqpage/<str:pk>/', views.faqpage, name="faq-page"),

    path('exportcsv/', views.exportcsv, name="export-csv"),
    path('exportassetscsv/', views.exportassets, name="export-assets"),

    path('deletemessage/<str:pk>/', views.deletemessage, name="delete-message"),

    path('checkoutpage/<str:pk>/', views.checkout, name="check-out"),

    path('users/', views.userpage, name="Users-page"),
    path('profilepage/<str:pk>', views.profilepage, name="profile-page"),


]
