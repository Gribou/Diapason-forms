from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class SafetyCubeRef(models.Model):
    reference = models.CharField(
        "Référence", null=True, blank=True, max_length=100)
    url = models.CharField("Lien SafetyCube", null=True,
                           blank=True, max_length=250)
    status = models.CharField(
        "Etat d'avancement", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Objet SafetyCube"
        verbose_name = "Objets SafetyCube"


class AbstractPostIt(models.Model):

    class Meta:
        abstract = True
        verbose_name = 'Post-it'
        verbose_name_plural = "Post-its"
        ordering = ['creation_date']

    def __str__(self):
        return self.content

    content = models.TextField("Contenu")
    author = models.ForeignKey(get_user_model(),
                               related_name="%(app_label)s_postits",
                               on_delete=models.SET_NULL,
                               null=True)
    creation_date = models.DateTimeField('Date de création', auto_now_add=True)
    update_date = models.DateTimeField('Date de mise à jour', auto_now=True)

    def get_parent(self):
        try:
            return self.parent.get_parent()
        except ObjectDoesNotExist:
            return None


class AbstractCounter(models.Model):
    ''' Long-term counter
        Used to count submitted forms
        A normal ManyToManyField would not do because we want to also remember completed form which have been/will be deleted from database
    '''
    class Meta:
        abstract = True
        ordering = ('-date', 'category')
        verbose_name = "Compteur"
        verbose_name_plural = "Statistiques"

    category = models.CharField(
        "Catégorie", null=False, blank=False, max_length=50)
    date = models.DateField("Date d'enregistrement")
    id_list_as_string = models.TextField(
        "Liste des fiches", help_text="Liste des identifiants uniques de fiche séparées par des points-virgules")

    def __str__(self):
        return "{} {} : {}".format(self.date.strftime("%d/%m/%Y"), self.category, self.count)

    @property
    def count(self):
        return len(self.list)

    @property
    def list(self):
        return [int(pk) for pk in self.id_list_as_string.split(";")] if len(self.id_list_as_string) > 0 else []

    def add(self, pk):
        if pk not in self.list:
            if len(self.id_list_as_string) > 0:
                self.id_list_as_string += ";" + str(pk)
            else:
                self.id_list_as_string = pk
            self.save()

    def remove(self, pk):
        self.is_list_as_string = ";".join(
            [str(p) for p in self.list if int(p) != int(pk)])
        self.save()


class KnownRedactors(models.Model):
    email = models.CharField("Adresse e-mail", max_length=100)
    fullname = models.CharField("Nom complet", max_length=100)
    team = models.CharField("Equipe", max_length=25)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('email', 'fullname', 'team')
        ordering = ['-update_date']
