# Generated by Django 4.2.3 on 2023-10-16 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaDFV',
            fields=[
                ('idG', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.TextField(max_length=255)),
                ('data', models.DateField()),
                ('valor', models.FloatField()),
                ('tipo', models.TextField(max_length=255)),
                ('empresa', models.IntegerField()),
                ('qtd_parcelas', models.IntegerField()),
            ],
        ),
    ]