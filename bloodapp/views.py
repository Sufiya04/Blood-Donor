from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout, update_session_auth_hash
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,'home.html')

def donor(request):
    if request.method=='POST':
        form=DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Registered Successfully')
    else:
        form=DonorForm()
    return render(request,'donor.html',{'form': form})

def recipient(request):
    if request.method=='POST':
        form=RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Blood Request Registered Successfully")
        else:
            print(form.errors)
    else:
        form=RecipientForm()
    return render(request,'recipient.html',{'form': form})

def dashboard(request):
    total_donor=Donor.objects.count()
    total_recipient=Recipient.objects.count()
    approved=Recipient.objects.filter(status="Approved").count()
    pending=Recipient.objects.filter(status='Pending').count()
    request=Recipient.objects.all().order_by('-id')
    return render(request,'dashboard.html', {
        'total_donor': total_donor,
        'total_recipient': total_recipient,
        'approved': approved,
        'pending': pending,
        'request': request
    })

def approve(request,id):
    req= get_object_or_404(Recipient, id=id)
    req.status= "Approved"
    req.save()
    return redirect('dashboard')

def donorlist(request):
    total= Donor.objects.count()
    list= Donor.objects.all()
    return render(request,'donorlist.html', {'total': total, 'list': list,})

def blood(request):
    total= Recipient.objects.count()
    request= Recipient.objects.filter(status="Pending").count()
    list= Recipient.objects.all()
    return render(request,'request.html', {'total': total, 'list': list,})

def approved(request):
    approve= Recipient.objects.filter(status="Approved").count()
    list= Recipient.objects.filter(status="Approved")
    return render(request,'approve.html', {'approve': approve, 'list': list})

def pending(request):
    pending= Recipient.objects.filter(status="Pending").count()
    list= Recipient.objects.filter(status="Pending")
    return render(request,'pending.html', {'pending': pending, 'list': list})

def units(request):
    stock= Donor.objects.values('blood').annotate(units=Count('blood'))
    return render(request, 'units.html', {'stock': stock})


def admin_signin(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'signin.html', {'form': form})

def admin_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(128600)
                else:
                    request.session.set_expiry(0)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                temp_password = get_random_string(length=8)
                user.set_password(temp_password)
                user.save()
                send_mail(
                    'Your Temporary Password',
                    f'Here is your temporary password: {temp_password}',
                    'admin@example.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'A temporary password has been sent to your email.')
                return redirect('admin')
            except User.DoesNotExist:
                form.add_error('email', 'No user found with this email address.')
    else:
        form = ResetPasswordForm()
        
    return render(request, 'reset.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin')