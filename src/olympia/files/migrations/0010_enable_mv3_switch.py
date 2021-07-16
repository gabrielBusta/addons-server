# Generated by Django 2.2.17 on 2021-01-12 16:14

from django.db import migrations


def create_waffle_switch(apps, schema_editor):
    Switch = apps.get_model("waffle", "Switch")

    Switch.objects.create(
        name="enable-mv3-submissions",
        active=False,
        note="Enable submission of addons with manifest_version:3",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0009_add_enable_manifest_normalization_switch'),
    ]

    operations = [migrations.RunPython(create_waffle_switch)]
