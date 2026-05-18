<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404, redirect
from .models import Warehouse, Inventory
from .forms import WarehouseForm


def index(request):
    """Home page - accessible at 127.0.0.1:8000/"""
    return render(request, 'inventory/index.html')


def add_new_record(request):
    """Add a new Warehouse record - accessible at /inventory/add-new-record"""
    success = False
    saved_name = ''

    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            saved_name = warehouse.name
            success = True
            form = WarehouseForm()  # reset form after success
    else:
        form = WarehouseForm()

    return render(request, 'inventory/addNewWarehouse.html', {
        'form': form,
        'success': success,
        'saved_name': saved_name,
    })


=======
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Warehouse, Inventory


@login_required
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
def warehouse_list(request):
    warehouses = Warehouse.objects.prefetch_related('inventory_items__product').all()
    return render(request, 'inventory/warehouse_list.html', {'warehouses': warehouses})


<<<<<<< HEAD
=======
@login_required
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    items = warehouse.inventory_items.select_related('product').all()
    return render(request, 'inventory/warehouse_detail.html', {'warehouse': warehouse, 'items': items})


<<<<<<< HEAD
=======
@login_required
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
def inventory_list(request):
    items = Inventory.objects.select_related('product', 'warehouse').all()
    low_stock = [i for i in items if i.needs_reorder]
    return render(request, 'inventory/inventory_list.html', {'items': items, 'low_stock': low_stock})
