from django.shortcuts import render, redirect
from order.models import Payment
from .forms import PaymentForm

def index(request):
    payments = Payment.objects.all()
    return render(request, 'payment_index.html', {'payments': payments})

def add_new_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment-index')
    else:
        form = PaymentForm()
    return render(request, 'addNewPayment.html', {'form': form})