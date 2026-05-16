from django.shortcuts import render,redirect
from doctors.models import ALLDOCTORS,Treatment
from doctors.forms import AppointmentForm

# Create your views here.
def alldoctors(request):
    doctors = ALLDOCTORS.objects.all()
    return render(request,"doctors/alldoctors.html",{'doctors':doctors})

def all_treatments(request):
    treatments = Treatment.objects.all()
    return render(request, 'doctors/alltreatments.html', {'treatments': treatments})

def doctors_by_treatments(request, treatment_id):
    treatment = Treatment.objects.get(id=treatment_id)
    doctors = ALLDOCTORS.objects.filter(treatment__id=treatment_id)

    return render(request, 'doctors/doctors_by_treatments.html', {
        'treatment': treatment,
        'doctors': doctors
    })

def book_appointment(request, doctor_id,treatment_id):
    doctor = ALLDOCTORS.objects.get(id=doctor_id)
    treatment = Treatment.objects.get(id=treatment_id)
    username = request.user 
    print(username) 
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = username
            appointment.doctor = doctor.name
            appointment.treatment = treatment.treatment_name
            appointment.save()
            return redirect('doctors:alldoctors')
        else:
            print(form.errors)
    else:
        form = AppointmentForm()

    return render(request, 'doctors/appointment_form.html', {'form': form,'doctor':doctor,'treatment':treatment})



# def book_appointment(request):
    # form = AppointmentForm()
    # return render(request,"appointment.html",{'form':form})