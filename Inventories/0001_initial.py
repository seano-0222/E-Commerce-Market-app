from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Depends on the products app migration that defines Product.
        # Update the migration name below if your products app uses a different initial migration.
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('warehouse_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField(
                    help_text='Maximum number of stock units this warehouse can hold.'
                )),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.ForeignKey(
                    help_text='The product being tracked in this inventory record.',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='inventories',
                    to='products.product',
                )),
                ('warehouse', models.ForeignKey(
                    help_text='The warehouse where this stock is stored.',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='inventories',
                    to='inventory.warehouse',
                )),
                ('quantity', models.PositiveIntegerField(
                    default=0,
                    help_text='Current stock quantity available in this warehouse.'
                )),
                ('reorder_threshold', models.PositiveIntegerField(
                    default=10,
                    help_text='Minimum quantity before a restock is triggered.'
                )),
                ('reorder_quantity', models.PositiveIntegerField(
                    default=50,
                    help_text='How many units to order when restocking.'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
                'ordering': ['warehouse', 'product'],
            },
        ),
        migrations.AddConstraint(
            model_name='inventory',
            constraint=models.UniqueConstraint(
                fields=('product', 'warehouse'),
                name='unique_product_warehouse',
            ),
        ),
    ]
