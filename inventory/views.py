from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Warehouse, Inventory


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.prefetch_related('inventory_items__product').all()
    return render(request, 'inventory/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    items = warehouse.inventory_items.select_related('product').all()
    return render(request, 'inventory/warehouse_detail.html', {'warehouse': warehouse, 'items': items})


@login_required
def inventory_list(request):
    items = Inventory.objects.select_related('product', 'warehouse').all()
    low_stock = [i for i in items if i.needs_reorder]
    return render(request, 'inventory/inventory_list.html', {'items': items, 'low_stock': low_stock})
