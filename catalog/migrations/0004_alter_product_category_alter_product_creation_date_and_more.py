# Generated by Django 4.2.3 on 2023-07-22 17:12

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='category name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=catalog.models.save_picture, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='purchase price'),
        ),
    ]
