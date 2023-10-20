from django.db import models

class OffenseLibrary(models.Model):
    name = models.CharField(max_length=1500)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Offense Library'
        verbose_name_plural = 'Offense Libraries'


class PlaceOfOmission(models.Model):
    place_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.place_name)

    class Meta:
        verbose_name = 'Place of Omission'
        verbose_name_plural = 'Place of Omission'

class PunishmentLibrary(models.Model):
    punishment = models.CharField(max_length=255)

    def __str__(self):
        return str(self.punishment)

    class Meta:
        verbose_name = 'Punishment Library'
        verbose_name_plural = 'Punishment Library'

class ImposedByWhom(models.Model):
    name = models.CharField(max_length=1500)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Imposed by Whom'
        verbose_name_plural = 'Imposed by Whom'

class Resolution(models.Model):
    # decision_of_appeal =
    pass

class Offense(models.Model):
    offense = models.ForeignKey(OffenseLibrary, related_name="offense_library", on_delete=models.DO_NOTHING)
    place = models.ForeignKey(PlaceOfOmission, related_name="place_of_omission", on_delete=models.DO_NOTHING)
    punishments = models.ManyToManyField(PunishmentLibrary, related_name="punishment_library")
    imposer = models.ManyToManyField(ImposedByWhom, related_name="imposed_by_whom")

    def __str__(self):
        return str(self.offense)

    class Meta:
        verbose_name = 'Offense Library'
        verbose_name_plural = 'Offense Libraries'
