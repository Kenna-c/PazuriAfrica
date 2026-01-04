from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment
from .daraja import stk_push
from accademics.models import Fee
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json

@login_required
def pay_fees(request):
    profile = request.user.profile
    fee = Fee.objects.get(student=profile)

    if request.method == 'POST':
        phone = request.POST['phone']
        amount = request.POST['amount']

        payment = Payment.objects.create(
            student=profile,
            amount=amount,
            phone_number=phone
        )

        stk_push(
            phone=phone,
            amount=amount,
            callback_url="https://yourdomain.com/payments/callback/",
            account_ref=profile.admission_number,
            desc="School Fees"
        )

        return render(request, 'payments/payment_pending.html')

    return render(request, 'payments/pay_fees.html', {'fee': fee})

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)

    callback = data['Body']['stkCallback']
    result_code = callback['ResultCode']

    if result_code == 0:
        items = callback['CallbackMetadata']['Item']
        receipt = next(i['Value'] for i in items if i['Name'] == 'MpesaReceiptNumber')
        amount = next(i['Value'] for i in items if i['Name'] == 'Amount')

        payment = Payment.objects.filter(
            status='Pending'
        ).last()

        payment.status = 'Completed'
        payment.receipt_number = receipt
        payment.save()

        fee = Fee.objects.get(student=payment.student)
        fee.paid_amount += amount
        fee.save()

    return JsonResponse({"status": "ok"})