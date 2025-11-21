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
            donor= form.save()
            stock, created= BloodStock.objects.get_or_create(blood = donor.blood)
            stock.units += donor.units
            stock.save()
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

@login_required
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

@login_required
def approve(request,id):
    req= Recipient.objects.get(id= id)
    stock, created= BloodStock.objects.get_or_create(blood= req.blood)
    if stock.units >= req.units:
        stock.units -= req.units
        stock.save()
        req.status= "Approved"
        req.save()
        return HttpResponse("Request Approved and Stock Updated Successfully")
    else:
        return HttpResponse("Not enough stock")

@login_required
def donorlist(request):
    total= Donor.objects.count()
    list= Donor.objects.all()
    return render(request,'donorlist.html', {'total': total, 'list': list,})

@login_required
def blood(request):
    total= Recipient.objects.count()
    request= Recipient.objects.filter(status="Pending").count()
    list= Recipient.objects.all()
    return render(request,'request.html', {'total': total, 'list': list,})

@login_required
def approved(request):
    approve= Recipient.objects.filter(status="Approved").count()
    list= Recipient.objects.filter(status="Approved")
    return render(request,'approve.html', {'approve': approve, 'list': list})

@login_required
def pending(request):
    pending= Recipient.objects.filter(status="Pending").count()
    list= Recipient.objects.filter(status="Pending")
    return render(request,'pending.html', {'pending': pending, 'list': list})

@login_required
def units(request):
    stock= BloodStock.objects.all()
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
            user = form.get_user() 
            login(request, user)
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600) 
            else:
                request.session.set_expiry(0)

            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html",{"form":form})

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