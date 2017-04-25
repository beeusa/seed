# !/usr/bin/env python
# encoding: utf-8
"""
:copyright (c) 2014 - 2016, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.  # NOQA
:author
"""
from celery import shared_task
from celery.utils.log import get_task_logger
from models import DataQualityCheck
from seed.data_importer.models import ImportFile
from seed.decorators import get_prog_key
from seed.utils.cache import set_cache

logger = get_task_logger(__name__)


@shared_task
def check_data_chunk(model, ids, file_pk, increment):
    """

    :param model: one of 'PropertyState' or 'TaxLotState'
    :param ids: list of primary key ids to process
    :param file_pk: import file primary key
    :param increment: currently unused, but needed because of the special method that appends this onto the function  # NOQA
    :return: None
    """

    qs = model.objects.filter(id__in=ids).iterator()
    import_file = ImportFile.objects.get(pk=file_pk)
    super_org = import_file.import_record.super_organization

    d = DataQualityCheck.retrieve(super_org.get_parent())
    d.check_data(model.__name__, qs)
    d.save_to_cache(file_pk)


@shared_task
def finish_checking(file_pk):
    """
    Chord that is called after the data quality check is complete

    :param file_pk: import file primary key
    :return:
    """

    prog_key = get_prog_key('check_data', file_pk)
    result = {
        'status': 'success',
        'progress': 100,
        'message': 'data quality check complete'
    }
    set_cache(prog_key, result['status'], result)
