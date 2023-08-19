# Generated by Django 4.2.3 on 2023-08-15 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_posts_options_alter_posts_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.SmallIntegerField(verbose_name='версия')),
                ('version_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='название версии')),
                ('is_current', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'Версия Продукта',
                'verbose_name_plural': 'Версии Продуктов',
                'ordering': ('version',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='current_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_version', to='catalog.productversion', verbose_name='текущая версия'),
        ),
    ]
