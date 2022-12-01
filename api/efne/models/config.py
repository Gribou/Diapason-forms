from django.db import models


class EventType(models.Model):
    name = models.CharField("Intitulé", max_length=20)
    rank = models.PositiveIntegerField("Ordre")
    is_tcas = models.BooleanField("TCAS", default=False)

    class Meta:
        verbose_name = "Type d'évènement"
        verbose_name_plural = "Types d'évènement"
        ordering = ['rank']

    def __str__(self):
        return self.name


class TechAction(models.Model):
    name = models.CharField("Intitulé", max_length=100)
    helperText = models.CharField(
        "Message d'aide", max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Action technique"
        verbose_name_plural = "Actions techniques"
        ordering = ['name']

    def __str__(self):
        return self.name


class TechEventType(models.Model):
    name = models.CharField("Intitulé", max_length=20)
    helperText = models.CharField("Message d'aide",
                                  max_length=250,
                                  null=True,
                                  blank=True)
    rank = models.PositiveIntegerField("Ordre")
    actions = models.ManyToManyField(TechAction,
                                     verbose_name="Actions à entreprendre",
                                     default=None,
                                     blank=True)

    class Meta:
        verbose_name = "Type d'évènement technique"
        verbose_name_plural = "Types d'évènement technique"
        ordering = ['rank']

    def __str__(self):
        return self.helperText if self.helperText else self.name


class Role(models.Model):
    label = models.CharField("Intitulé", max_length=10, unique=True)
    rank = models.PositiveIntegerField("Ordre", default=0)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ("rank", "label", )
