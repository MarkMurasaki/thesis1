# Generated by Django 4.1.7 on 2023-11-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
