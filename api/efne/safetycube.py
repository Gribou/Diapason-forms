from constance import config

from shared.safetycube.constants import SAFETYCUBE_FORMID
from shared.safetycube.utils import FormFormatter

# FIXME pièces jointes ?

# chr_1_6 (CWP) est prévu pour 4F apparemment...

TCAS_AIRCRAFT_TEMPLATE = """
Aéronef {} : {} (SSR {})
Phase de vol : {}
FL assigné : {}
FL réel : {}
A l'origine du signalement : {}
Type d'avis: {}
Contact Radio: {}
VFR: {}
Militaire: {}
"""

TCAS_REPORT_TEMPLATE = """
Compte-rendu d'évènement TCAS : 
{}
Analyse Pilote :
Distance minimale : {} NM
Altitude minimale : {} ft

Analyse Contrôleur :
Distance minimale : {} NM
Altitude minimale : {} ft

Y a-t-il eu une information de trafic ? {}
Sur demande du pilote ? {}
Si OUI, la demande a-t-elle été faite avant ou après la manoeuvre ? {}
A votre avis, l'action du pilote était-elle justifiée ? {}
Cet évènement a-t-il perturbé votre gestion du trafic ? {}
L'un des pilotes a-t-il signalé vouloir rédiger un ASR ? {}
Le filet de sauvegarde s'est-il déclenché ? {}
"""


class FneFormatter(FormFormatter):

    def make_fields(self, form):
        description = generate_description(form)
        title = self.make_title(form)
        fields = {
            'TITLE_DUPLICATED': title,
            'chr_1_0': form.event_date.strftime("%H:%M"),
            'chr_1_1': generate_team(form),
            'chr_1_2': "OUI" if form.isp else "NON",
            'chr_1_3': form.secteur,
            'chr_1_4': form.regroupement,
            'chr_1_5': form.position,
            'chr_1_9': form.lieu,
            'txt_1_0': description,
            'txt_1_0_DUPLICATED': description,
            'txt_1_1': form.cds_report.com_cds if hasattr(form, 'cds_report') else None,
            'cbx_3_0_0': check_tech_actions(form, "LPLN"),
            'cbx_3_0_1': check_tech_actions(form, "XFPL"),
            'cbx_3_0_2': check_tech_actions(form, "LVOL"),
            'cbx_3_0_3': check_tech_actions(form, "Vidage"),
            'cbx_3_0_4': check_tech_actions(form, "TACT"),
        }
        fields.update(generate_aircrafts(form))
        return fields

    def make_title(self, fne):
        # "Y-m-d secteur lieu type1 type2 callsign1 callsign2"
        title = [fne.event_date.strftime("%Y%m%d")]
        if fne.secteur:
            title.append(fne.secteur)
        if fne.lieu:
            title.append(fne.lieu)
        title.extend([t.name.replace(" ", "_") for t in fne.event_types.all()])
        title.extend([a.callsign for a in fne.aircrafts.all()])
        return " ".join(title)


def generate_description(fne):
    description = "{}\n\n".format(fne.description)
    if fne.event_types.exists():
        event_types = ", ".join([t.name
                                 for t in fne.event_types.all()])
        description += "Type d'évènement : {}\n".format(event_types)
    if hasattr(fne, "cds_report"):
        if fne.cds_report.rex_cds:
            description += "REX CDS : OUI\n"
        if fne.cds_report.notif_rpo:
            description += "Notification RPO : OUI\n"
        if fne.cds_report.cpi:
            description += "Constat Préalable d'Infraction : OUI\n"
    if fne.tech_actions_done.exists():
        actions = ", ".join([a.name for a in fne.tech_actions_done.all()])
        description += "Actions techniques entreprises : {}\n".format(actions)
    if hasattr(fne, "tcas_report"):
        aircrafts = ""
        for i, a in enumerate(fne.tcas_report.aircrafts.all()):
            aircrafts += TCAS_AIRCRAFT_TEMPLATE.format(
                i+1, a.callsign, a.ssr or "?",
                a.get_flight_phase_display(), a.assigned_fl or "?", a.real_fl or "?",
                "OUI" if a.is_origin else "NON",
                a.get_advisory_type_display(),
                "OUI" if a.contact_radio else "NON",
                "OUI" if a.is_vfr else "NON",
                "OUI" if a.is_mil else "NON")

        description += TCAS_REPORT_TEMPLATE.format(
            aircrafts,
            fne.tcas_report.pilote_min_distance,
            fne.tcas_report.pilote_min_altitude,
            fne.tcas_report.ctl_min_distance, fne.tcas_report.ctl_min_altitude,
            "OUI" if fne.tcas_report.traffic_info else "NON",
            "OUI" if fne.tcas_report.pilot_request else "NON",
            "AVANT" if fne.tcas_report.before_manoeuvre else "APRES",
            "OUI" if fne.tcas_report.pilot_action_required else "NON",
            "OUI" if fne.tcas_report.disrupted_traffic else "NON",
            "OUI" if fne.tcas_report.asr else "NON",
            "OUI" if fne.tcas_report.safety_net else "NON")
    return description


def generate_team(form):
    return '/'.join(form.redactors.order_by('team').values_list('team__label', flat=True).distinct().all())


def generate_redactors(form):
    return ', '.join(form.redactors.values_list('fullname', flat=True).all())


def check_tech_actions(fne, action_type):
    for action in fne.tech_actions_done.all():
        if action_type.lower() in action.name.lower():
            return True


def generate_aircrafts(fne):
    return {"CALLSIGN{}".format("" if i == 0 else "_{}".format(i)): a.callsign for i, a in enumerate(fne.aircrafts.all())}
