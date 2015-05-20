from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ('name', )


class Relationship(models.Model):
    start = models.ForeignKey(Unit, related_name='start_id', default=None)
    end = models.ForeignKey(Unit, related_name='end_id', default=None)
    value = models.IntegerField()

    def __unicode__(self):
        return u'%s - %s (%s)' % (self.start, self.end, self.value)
    class Meta:
        ordering = ('start',)

