# Generated by Django 5.0.6 on 2024-07-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_notificationmodel_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationmodel',
            name='text',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
