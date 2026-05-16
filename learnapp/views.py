from django.shortcuts import render,redirect
from learnapp.forms import UserForm,UserProfileForm,UserUpdateForm,UserProfileUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doctors.models import Appointment
from labreports.models import LabTecnicians
from learnapp.models import UserDetails

# Create your views here.
def registeration(request):
    registered = False
    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user =form1.save()
            user.set_password(user.password)
            user.save()

            profile = form2.save(commit=False)
            profile.user = user # user=form1.save()
            profile.save()
            registered = True

    else:
        form1 =UserForm()
        form2 = UserProfileForm()
        
    return render(request,"registeration.html",{'form1':form1,'form2':form2,'registered': registered })


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)

                # ✅ Check if Lab Technician
                if LabTecnicians.objects.filter(user=user).exists():
                    return redirect('labtech_home')
                
                # ✅ Check if Patient
                elif UserDetails.objects.filter(user=user).exists():
                    return redirect('home')

                # ✅ Default fallback
                else:
                    return redirect('login')

            else:
                return HttpResponse("User is not active")

        else:
            return HttpResponse("Please check your credentials...!!!")

    return render(request,"login.html",{})

@login_required(login_url="login")
def home(request):
    return render(request,"home.html",{})

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile(request):

    user = request.user

    # Get or create UserDetails
    try:
        user_details = user.userdetails
    except UserDetails.DoesNotExist:
        user_details = None

    # Patient appointments
    appointments = Appointment.objects.filter(
        user=user
    )

    # Check if technician exists
    technician = None

    if LabTecnicians.objects.filter(
        user=user
    ).exists():

        technician = LabTecnicians.objects.get(
            user=user
        )

    return render(
        request,
        "profile.html",
        {
            'user': user,
            'user_details': user_details,
            'appointments': appointments,
            'technician': technician
        }
    )


@login_required(login_url="login")
def update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)
        form1 =UserProfileUpdateForm(request.POST,request.FILES,instance=request.user.userdetails)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user) # instance=request.user :- This for Autofill of username and email From Database
        form1 = UserProfileUpdateForm(instance=request.user.userdetails) # instance=request.user.userdetails :- This is for autofill of UserDetails from Database Values Likes phone,address,street etc
    context = {
        'form':form,
        'form1':form1
    }
    return render(request,"update.html",context)


