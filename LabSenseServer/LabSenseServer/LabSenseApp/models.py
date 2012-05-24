from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Channel(models.Model):

    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("index", (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Channel, self).save(*args, **kwargs)

class Sensor(models.Model):

    name = models.CharField(max_length=20)
    measurement = models.CharField(max_length=20)
    value = models.FloatField()

    channel = models.ForeignKey("Channel")

    def __unicode__(self):
        return self.name
