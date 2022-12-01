from constance import config

from shared.safetycube.constants import SAFETYCUBE_FORMID
from shared.safetycube.utils import FormFormatter


class SimiFormatter(FormFormatter):

    def make_fields(self, form):
        description = generate_description(form)
        title = self.make_title(form)
        fields = {
            'TITLE_DUPLICATED': title,
            'chr_1_0': form.event_date.strftime("%H:%M"),
            'chr_1_1': generate_team(form),
            'txt_1_0': description,
            'txt_1_0_DUPLICATED': description,
        }
        fields.update(generate_aircrafts(form))
        return fields

    def make_title(self, simi):
        # "Y-m-d similitude callsign1 callsign2"
        title = [simi.event_date.strftime("%Y%m%d"), "Similitude"]
        title.extend([a.callsign for a in simi.aircrafts.all()])
        return " ".join(title)


def generate_description(simi):
    description = "Similitude d'indicatifs\n\n{}\n\n".format(simi.description)
    if simi.with_incident:
        description += "Avec incident : OUI\n"
    for a in simi.aircrafts.all():
        description += "Position de {} : FL{}, {}\n".format(
            a.callsign, a.fl, a.position)
    return description


def generate_team(form):
    return '/'.join(form.redactors.order_by('team').values_list('team__label', flat=True).distinct().all())


def generate_aircrafts(simi):
    fields = {}
    for i, a in enumerate(simi.aircrafts.all()):
        index_suffix = "" if i == 0 else "_{}".format(i)
        fields.update({
            "CALLSIGN{}".format(index_suffix): a.callsign,
            "AIRCRAFT_TYPE{}".format(index_suffix): a.type,
            "CODE_SSR{}".format(index_suffix): a.ssr,
            "CITY_FROM{}".format(index_suffix): a.provenance,
            "CITY_TO{}".format(index_suffix): a.destination,
        })
    return fields
