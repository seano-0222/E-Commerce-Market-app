from django.shortcuts import render, redirect
from order.models import Shipment
from .forms import ShipmentForm

def index(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipment_index.html', {'shipments': shipments})

def add_new_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shipment-index')
    else:
        form = ShipmentForm()
    return render(request, 'addNewShipment.html', {'form': form})