# Generated by Django 2.1.5 on 2019-01-13 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190113_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='step',
            name='description',
            field=models.TextField(),
        ),
    ]
