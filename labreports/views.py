from django.shortcuts import render, redirect,get_object_or_404
from labreports.forms import LabTechniciansForm, LabTestsForm
from learnapp.models import UserDetails
from doctors.models import ALLDOCTORS
from labreports.models import LabTecnicians
from labreports.models import LabTests,ALL_LAB_TESTS,TEST_STATUS,RESULT_RANGE
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

ALL_LAB_TESTS = [
    ('CBC', 'Complete Blood Count'),
    ('LFT', 'Liver Function Test'),
    ('URINE_TOTAL', 'Urine Total Test'),
    ('URINE_MICRO', 'Urine Microscopic'),
    ('SERUM', 'Serum Routine'),
    ('THYROID', 'Thyroid'),
]

LAB_TEST_PRICE = {
    'CBC': 500,
    'LFT': 700,
    'URINE_TOTAL': 150,
    'URINE_MICRO': 200,
    'SERUM': 350,
    'THYROID': 800,
}

LAB_TEST_TIME = {
    'CBC': '4 hr',
    'LFT': '8 hr',
    'URINE_TOTAL': '2 hr',
    'URINE_MICRO': '3 hr',
    'SERUM': '5 hr',
    'THYROID': '12 hr',
}

def register_lab_technician(request):
    if request.method == 'POST':
        form = LabTechniciansForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.save()

            technician = LabTecnicians(
                user=user, 
                emp_id=form.cleaned_data['emp_id'],
                qualification=form.cleaned_data['qualification'],
                year_of_experience=form.cleaned_data['year_of_experience'],
                address=form.cleaned_data['address']
            )
            technician.save()
            return redirect('login')

    else:
        form = LabTechniciansForm()

    return render(request, 'technician/technicianregister.html', {
        'form': form,
    })



@login_required
def labtech_home(request):

    technician = LabTecnicians.objects.get(
        user=request.user
    )

    return render(
        request,
        'technician/labtech_home.html',
        {
            'technician': technician
        }
    )


def all_lab_tests(request):

    tests_data = []

    for code, name in ALL_LAB_TESTS:

        tests_data.append({

            'name': code,

            'price': LAB_TEST_PRICE.get(code),

            'time': LAB_TEST_TIME.get(code),

        })

    return render(
        request,
        'technician/all_tests.html',
        {
            'tests': tests_data
        }
    )


# Technician DashBoard Start From Here
# Techcian Work Start From Here
@login_required
def lab_dashboard(request):

    # Get all tests
    technician = LabTecnicians.objects.filter(user=request.user).first()

    if not technician:
        return redirect('login')

    records = LabTests.objects.all().order_by('created_at')
    paginator = Paginator(records,5)
    page_number = request.GET.get('pg')
    records = paginator.get_page(page_number)

    return render(request, 'technician/lab_dashboard.html', {
        'records': records
    })


@login_required
def add_test(request):
    doctors = ALLDOCTORS.objects.all()
    patients = UserDetails.objects.all()

    if request.method == "POST":
        # 🔥 Get IDs from form
        doctor_id = request.POST.get('refered_by')
        patient_id = request.POST.get('patient_name')

        # 🔥 Convert ID → Objects
        doctor = ALLDOCTORS.objects.get(id=doctor_id)
        patient = UserDetails.objects.get(id=patient_id)

        # 🔥 Create Lab Test
        LabTests.objects.create(
            reffered_by=doctor,
            patient_name=patient,
            lab_test=request.POST.get('lab_test'),
            lab_result=request.POST.get('lab_result'),
            result_range=request.POST.get('result_range'),
            result_desc=request.POST.get('result_desc'),
            test_cost=request.POST.get('test_cost')
        )

        return redirect('lab_dashboard')  # or wherever your list page is

    context = {
        'doctors': doctors,
        'patients': patients,
        'lab_tests': ALL_LAB_TESTS,
        'status_choices': TEST_STATUS,
        'range_choices': RESULT_RANGE
    }

    return render(request, "technician/add_lab_test.html", context)



@login_required
def edit_test(request, id):
    technician = LabTecnicians.objects.filter(user=request.user).first()

    if not technician:
        return redirect('login')

    test = LabTests.objects.get(id=id)

    if request.method == 'POST':
        test.lab_result = request.POST.get('lab_result')

        # ✅ FIX: don't overwrite with None
        test.result_range = request.POST.get('result_range') or test.result_range

        test.result_desc = request.POST.get('result_desc')
        test.save()

        return redirect('lab_dashboard')

    return render(request, 'technician/edit_lab_test.html', {'test': test,'range_choices': RESULT_RANGE })