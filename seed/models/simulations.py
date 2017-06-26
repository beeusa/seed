# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2017, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""
from __future__ import unicode_literals

import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

# from seed.models.measures import Measure

logger = logging.getLogger(__name__)


class Simulation(models.Model):
    """
    Simulation contains results from a simulation. Presenty there is only one type of simulation
    with a maximum of one object per PropertyState.

    Data are stored in a JSONField and there can be mulitple result files.
    """

    # currently only one simulation result object for each propertystate
    property_state = models.OneToOneField("PropertyState", on_delete=models.CASCADE,
                                          primary_key=True, )
    data = JSONField(default=dict, blank=True)


class ResultFile(models.Model):
    # TODO: Upload to result_files/{ id of property_state }
    simulation = models.ForeignKey(Simulation, related_name='files')
    file = models.FileField(upload_to="simulation_files", max_length=500, blank=True, null=True)
    file_size_in_bytes = models.IntegerField(blank=True, null=True)
