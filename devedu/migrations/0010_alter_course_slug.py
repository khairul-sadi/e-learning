# Generated by Django 4.1.4 on 2023-07-24 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("devedu", "0009_alter_course_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course", name="slug", field=models.SlugField(unique=True),
        ),
    ]