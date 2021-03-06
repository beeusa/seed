# encoding: utf-8
"""
:copyright (c) 2014 - 2019, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
"""

from django.db import models

from seed.models import Property

from quantityfield.fields import QuantityField


class Meter(models.Model):
    COAL_ANTHRACITE = 1
    COAL_BITUMINOUS = 2
    COKE = 3
    DIESEL = 4
    DISTRICT_CHILLED_WATER = 5
    DISTRICT_HOT_WATER = 6
    DISTRICT_STEAM = 7
    ELECTRICITY = 8
    ELECTRICITY_ON_SITE_RENEWABLE = 9
    FUEL_OIL_NO_1 = 10
    FUEL_OIL_NO_2 = 11
    FUEL_OIL_NO_4 = 12
    FUEL_OIL_NO_5_AND_NO_6 = 13
    KEROSENE = 14
    NATURAL_GAS = 15
    OTHER = 16
    PROPANE = 17
    WOOD = 18

    # Taken from https://portfoliomanager.zendesk.com/hc/en-us/articles/211025388-Is-there-a-list-of-valid-property-level-energy-meter-types-and-unit-of-measure-combinations-
    ENERGY_TYPES = (
        (COAL_ANTHRACITE, 'Coal (anthracite)'),
        (COAL_BITUMINOUS, 'Coal (bituminous)'),
        (COKE, 'Coke'),
        (DIESEL, 'Diesel'),
        (DISTRICT_CHILLED_WATER, 'District Chilled Water'),  # This isn't copied exactly
        (DISTRICT_HOT_WATER, 'District Hot Water'),
        (DISTRICT_STEAM, 'District Steam'),
        (ELECTRICITY, 'Electricity'),
        (ELECTRICITY_ON_SITE_RENEWABLE, 'Electricity - on site renewable'),
        (FUEL_OIL_NO_1, 'Fuel Oil (No. 1)'),
        (FUEL_OIL_NO_2, 'Fuel Oil (No. 2)'),
        (FUEL_OIL_NO_4, 'Fuel Oil (No. 4)'),
        (FUEL_OIL_NO_5_AND_NO_6, 'Fuel Oil (No. 5 & No. 6)'),
        (KEROSENE, 'Kerosene'),
        (NATURAL_GAS, 'Natural Gas'),
        (OTHER, 'Other'),
        (PROPANE, 'Propane and Liquid Propane'),
        (WOOD, 'Wood'),
    )

    type_lookup = dict((reversed(type) for type in ENERGY_TYPES))

    PORTFOLIO_MANAGER = 1
    GREENBUTTON = 2
    BUILDINGSYNC = 3

    SOURCES = (
        (PORTFOLIO_MANAGER, 'Portfolio Manager'),
        (GREENBUTTON, 'GreenButton'),
        (BUILDINGSYNC, 'BuildingSync'),
    )

    is_virtual = models.BooleanField(default=False)

    property = models.ForeignKey(
        Property,
        related_name='meters',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    source = models.IntegerField(choices=SOURCES, default=None, null=True)
    source_id = models.CharField(max_length=255, null=True, blank=True)

    type = models.IntegerField(choices=ENERGY_TYPES, default=None, null=True)


class MeterReading(models.Model):
    meter = models.ForeignKey(
        Meter,
        related_name='meter_readings',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    start_time = models.DateTimeField(db_index=True, primary_key=True)
    end_time = models.DateTimeField(db_index=True)

    reading = QuantityField('kBtu')

    # The following two fields are tracked for historical purposes
    source_unit = models.CharField(max_length=255, null=True, blank=True)
    conversion_factor = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('meter', 'start_time', 'end_time')
