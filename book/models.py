from django.db import models
from django.utils import timezone
from book.utils.date_formatter import date_formatter2

class OffenseLibrary(models.Model):
    violation = models.TextField(blank=False, null=True, help_text='ex: Violation of R.A 7877 (Anti-Sexual Harassment Act of 1995) and R.A 11313 (Safe Spaces Act)')

    def __str__(self):
        return str(self.violation)

    class Meta:
        verbose_name = 'Offense Library'
        verbose_name_plural = 'Offense Libraries'


class PlaceOfOmission(models.Model):
    place = models.CharField(max_length=255, default="CJVAB, Pasay City")
    date = models.DateTimeField(default=timezone.now, editable=True)

    def __str__(self):
        return date_formatter2(str(self.date)) + ' - ' + str(self.place)

    class Meta:
        verbose_name = 'Date & Place of Omission'
        verbose_name_plural = 'Date & Place of Omission'

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
    decision_of_appeal = models.TextField(blank=True, null=True)
    mitigation_re_remission = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True,)
    intl_first_sergeant = models.CharField(max_length=250, blank=True, null=True)
    initial_of_ep = models.CharField(max_length=50, blank=True, null=True)


class AFP_Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    afpsn = models.CharField(max_length=50, null=True, default=None)
    last_name = models.CharField(max_length=50, null=True, default=None)
    first_name = models.CharField(max_length=50, null=True, default=None)
    middle_name = models.CharField(max_length=50, null=True, default=None)
    rank_id = models.CharField(max_length=50, null=True, default=None)

    def __str__(self):
        return str(self.rank_id) + " " + str(self.last_name) + ", " + \
            str(self.first_name) + " " + str(self.middle_name) + " " + str(self.afpsn)

    class Meta:
        db_table = 'afp_personnel'
        verbose_name = 'AFP Personnel'
        verbose_name_plural = 'AFP Personnel\'s'


class Offense(models.Model):
    objects = None
    personnel = models.ForeignKey(AFP_Personnel, related_name="afp_personnel", on_delete=models.DO_NOTHING, null=True)
    offense = models.ManyToManyField(OffenseLibrary, related_name="offense_library")
    place = models.ForeignKey(PlaceOfOmission, related_name="place_of_omission", on_delete=models.DO_NOTHING)
    punishments = models.ManyToManyField(PunishmentLibrary, related_name="punishment_library")
    imposer = models.ManyToManyField(ImposedByWhom, related_name="imposed_by_whom")
    resolution = models.ManyToManyField(Resolution, related_name="resolution", blank=True)
    entry_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.offense)

    class Meta:
        verbose_name = 'Submitted Offense'
        verbose_name_plural = 'Submitted Offense'
