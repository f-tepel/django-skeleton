from django.shortcuts import render


def verify_email(request):
    return render(request, 'verify_email.html')