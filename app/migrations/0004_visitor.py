# Generated by Django 2.2.7 on 2020-01-30 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191217_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=200)),
                ('person', models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='app.Person')),
                ('visitor', models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to='app.Person')),
            ],
        ),
    ]
