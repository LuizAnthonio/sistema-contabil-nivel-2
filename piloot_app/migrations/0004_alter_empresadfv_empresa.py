# Generated by Django 4.2.3 on 2023-10-18 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piloot_app', '0003_alter_empresadfv_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresadfv',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piloot_app.empresa'),
        ),
    ]
