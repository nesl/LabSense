from django.db import models
from django.template.defaultfilters import slugify

# Managers
class ChannelManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(slug=name)

# Models
class Channel(models.Model):

    # Channel manager
    objects = ChannelManager()

    # name is Raritan, Zwave, Veris, etc..
    name = models.CharField(max_length=20)

    # Title is title of page
    title = models.CharField(max_length=20)

    # slug is url
    slug = models.SlugField(blank=True)

    # Number of sensors for this measurement
    num_sensors = models.DecimalField(max_digits=6, decimal_places=4)


    def __unicode__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Channel, self).save(*args, **kwargs)

class Measurement(models.Model):

    # name is current, voltage, etc
    name = models.CharField(max_length=20)

    # slug if url version
    slug = models.SlugField(blank=True)

    # units if mA, volts, etc
    units = models.CharField(max_length=20)

    channel = models.ForeignKey("Channel")

    # slug is url
    #slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.slug

class SensorValue(models.Model):

    value = models.FloatField()

    measurement = models.ForeignKey("Measurement")

    def __unicode__(self):
        return self.value

