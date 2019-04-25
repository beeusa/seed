# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-20 01:54
from __future__ import unicode_literals

from django.db import migrations, models


def reassociate_labels_to_views(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    PropertyView = apps.get_model("seed", "PropertyView")
    property_views = PropertyView.objects.using(db_alias).all().prefetch_related('property')
    for p_view in property_views:
        labels = [l for l in p_view.property.labels.all()]
        p_view.labels.set(labels)

    TaxLotView = apps.get_model("seed", "TaxLotView")
    taxlot_views = TaxLotView.objects.using(db_alias).all().prefetch_related('taxlot')
    for tl_view in taxlot_views:
        labels = [l for l in tl_view.taxlot.labels.all()]
        tl_view.labels.set(labels)


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0102_auto_20190331_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyview',
            name='labels',
            field=models.ManyToManyField(to='seed.StatusLabel'),
        ),
        migrations.AddField(
            model_name='taxlotview',
            name='labels',
            field=models.ManyToManyField(to='seed.StatusLabel'),
        ),
        migrations.RunPython(reassociate_labels_to_views),
        migrations.RemoveField(
            model_name='taxlot',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='property',
            name='labels',
        ),
    ]