# Generated by Django 3.2.6 on 2021-11-24 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_dishes_workpiece'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehouse',
            options={'verbose_name': 'Склад', 'verbose_name_plural': 'Склад'},
        ),
        migrations.AddField(
            model_name='dishes',
            name='workpiece',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.workpieces', verbose_name='Заготовка'),
            preserve_default=False,
        ),
    ]
