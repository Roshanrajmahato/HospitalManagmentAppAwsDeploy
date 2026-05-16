import json

import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import DischargeSummary
from .forms import DischargeSummaryForm


# ==========================================
# 1️⃣ CREATE DISCHARGE
# ==========================================
@login_required(login_url='login')
def create_discharge(request):

    if request.method == "POST":

        form = DischargeSummaryForm(request.POST)

        if form.is_valid():

            discharge = form.save()

            print("✅ SAVED:", discharge.id)

            return redirect(
                'discharge_bill',
                pk=discharge.pk
            )

        else:

            print("❌ FORM ERRORS:", form.errors)

    else:

        form = DischargeSummaryForm()

    return render(
        request,
        "payment/create_discharge.html",
        {'form': form}
    )

# ==========================================
# 2️⃣ BILL DISPLAY VIEW
# ==========================================

@login_required(login_url='login')
def discharge_bill(request, pk):

    bill = get_object_or_404(

        DischargeSummary,
        pk=pk

    )

    return render(

        request,
        "payment/discharge_bill.html",
        {'bill': bill}

    )


# ==========================================
# 3️⃣ RAZORPAY ORDER CREATE
# ==========================================

@login_required(login_url='login')
def create_payment_order(request, pk):

    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    bill = get_object_or_404(DischargeSummary, pk=pk)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    amount = int(round(bill.grand_total * 100))

    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': f'bill_{bill.pk}',
        'payment_capture': 1,
        'notes': {
            'bill_id': str(bill.pk),
            'patient': str(bill.patient),
        },
    }

    order = client.order.create(data=order_data)

    return JsonResponse({
        'order_id': order.get('id'),
        'amount': amount,
        'currency': order.get('currency', 'INR'),
        'key_id': settings.RAZORPAY_KEY_ID,
        'name': 'Healthcare Hospital',
        'description': f'Discharge Bill #{bill.pk}',
        'bill_id': bill.pk,
    })


# ==========================================
# 4️⃣ RAZORPAY PAYMENT SUCCESS
# ==========================================

@login_required(login_url='login')
def payment_success(request):

    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON body.')

    required_fields = [
        'razorpay_payment_id',
        'razorpay_order_id',
        'razorpay_signature',
        'bill_id',
    ]

    if not all(field in data for field in required_fields):
        return HttpResponseBadRequest('Missing required payment fields.')

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature'],
        })

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({
            'success': False,
            'message': 'Payment verification failed. Please contact support.',
        }, status=400)

    return JsonResponse({
        'success': True,
        'message': 'Payment completed successfully.',
        'bill_id': data['bill_id'],
    })


# ==========================================
# 5️⃣ BILL LIST VIEW
# ==========================================

@login_required(login_url='login')
def discharge_list(request):

    bills = DischargeSummary.objects.all().order_by('-created_at')

    return render(

        request,
        "payment/discharge_list.html",
        {'bills': bills}

    )