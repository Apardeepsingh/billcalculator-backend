# Generated by Django 4.2.7 on 2023-11-19 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_itemprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='itemPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
