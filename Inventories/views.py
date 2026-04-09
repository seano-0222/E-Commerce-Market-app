from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Inventory, Warehouse


@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related('product', 'warehouse').all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})


@login_required
def inventory_detail(request, inventory_id):
    inventory = get_object_or_404(
        Inventory.objects.select_related('product', 'warehouse'),
        pk=inventory_id,
    )
    return render(request, 'inventory/inventory_detail.html', {'inventory': inventory})


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.prefetch_related('inventories').all()
    return render(request, 'inventory/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_detail(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    return render(request, 'inventory/warehouse_detail.html', {'warehouse': warehouse})
