# Generated by Django 2.0.7 on 2019-09-09 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Num', models.TextField(default='Number here')),
                ('Input', models.TextField(default='Whats on your mind')),
            ],
        ),
    ]
