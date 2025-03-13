# Generated by Django 4.2.20 on 2025-03-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod1', '0002_user_delete_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
