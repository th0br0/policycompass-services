from django.db import models

import datetime
import logging
from .managers import MetricManager, RawDataManager
from .utils import get_rawdata_for_metric, save_rawdata_for_metric

log = logging.getLogger(__name__)

class UnitCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Unit Category"
        verbose_name_plural = "Unit Categories"

    def __unicode__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    unit_category = models.ForeignKey(UnitCategory)

    def __unicode__(self):
        return self.title


class Metric(models.Model):

    objects = MetricManager()

    # Meta Data by User Input
    title = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    keywords = models.CharField(max_length=400)

    geo_location = models.CharField(max_length=1000, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    details_url = models.URLField(max_length=500, blank=True)
    license = models.CharField(max_length=100, blank=True)

    user_id = models.IntegerField()
    language_id = models.IntegerField()
    ext_resource_id = models.IntegerField(blank=True)

    # Auto-Generated Meta Data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(editable=False)

    # Data
    formula = models.CharField(max_length=10000, default='1')
    issued = models.DateField()

    unit = models.ForeignKey(Unit)

    _rawdata = None

    @property
    def rawdata(self):
        return get_rawdata_for_metric(self)


    @rawdata.setter
    def rawdata(self, value):
        self._rawdata = value


    @rawdata.deleter
    def rawdata(self):
        pass


    def save(self, *args, **kwargs):

        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            self.version += 1

        super(Metric, self).save(*args, **kwargs)
        save_rawdata_for_metric(self, self._rawdata)


    def __unicode__(self):
        return self.title


class MetricInDomain(models.Model):
    domain_id = models.IntegerField()
    metric = models.ForeignKey(Metric)

    class Meta:
        verbose_name = "Metric in Domain"
        verbose_name_plural = "Metrics in Domains"

    def __unicode__(self):
        return str(self.domain_id)


class RawData(models.Model):

    objects = RawDataManager()

    metric = models.ForeignKey(Metric)
    # Saving the row number, not necessary but convenient
    row = models.PositiveIntegerField()
    value = models.FloatField()
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        verbose_name = "Raw Data"
        verbose_name_plural = "Raw Data"
        ordering = ['row']


    def __unicode__(self):
        return str(self.row) + " Raw Data for " + self.metric.title


class RawDataCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Raw Data Category"
        verbose_name_plural = "Raw Data Categories"

    def __unicode__(self):
        return self.title


class RawDataExtra(models.Model):
    metric = models.ForeignKey(Metric)
    category = models.ForeignKey(RawDataCategory)

    class Meta:
        verbose_name = "Raw Data Extra"
        verbose_name_plural = "Raw Data Extras"

    def __unicode__(self):
        return str(self.metric) + " - " + str(self.category)


class RawDataExtraData(models.Model):
    raw_data_extra = models.ForeignKey(RawDataExtra)
    # Saving the row number, not necessary but convenient
    row = models.PositiveIntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Raw Data Extra Data"
        verbose_name_plural = "Raw Data Extra Data"
        ordering = ['row']

    def __unicode__(self):
        return str(self.row) + " " + str(self.raw_data_extra)





