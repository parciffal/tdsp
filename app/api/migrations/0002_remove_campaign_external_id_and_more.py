# Generated by Django 4.1.6 on 2023-03-28 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='external_id',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='verify_code',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='frequency_capping',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='super_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.category'),
        )
    ]