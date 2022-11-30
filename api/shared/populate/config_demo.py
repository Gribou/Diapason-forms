# --------------------------------------------------------------------
# Statuts possibles pour une fiche

DRAFT = "Brouillon"
WAITING = "En attente"
IN_PROGRESS = "En traitement"
DONE = "Traitée"
TO_BE_DELETED = "A supprimer"

STATUS_LIST = [{
    'label': DRAFT,
    'is_draft': True
}, {
    'label': WAITING,
    'is_waiting': True
}, {
    'label': IN_PROGRESS,
    'is_in_progress': True
}, {
    'label': DONE,
    'is_done': True
}, {
    'label': TO_BE_DELETED,
    'is_to_be_deleted': True
}]

# --------------------------------------------------------------------
# Possibilités pour la zone de qualification
ZONES = ['E', 'W']
TEAM_COUNT_PER_ZONE = 4

# --------------------------------------------------------------------
# Groupes d'utilisateurs

CDS = "Chef de Salle"
QSE = "QSS Enquête"
QSA = "QSS Analyse"
ETU = "Sub Etudes"
GROUPS = [
    {
        'name': CDS,
        'is_validator': True
    },
    {
        'name': QSE,
        'is_investigator': True,
        'has_all_access': True
    },
    {
        'name': QSA,
        'is_investigator': True,
        'has_all_access': True
    },
    {
        'name': ETU,
        'is_investigator': True,
    },
]
USERS = {
    'cds': CDS,
    'qse': QSE,
    'qsa': QSA,
    'etu': ETU,
}

NOT_VALIDATOR_GROUPS = [
    g for g in GROUPS if not g.get('is_validator', False)
]


def other_groups(group):
    return [g for g in NOT_VALIDATOR_GROUPS if g['name'] != group]


def make_transfer_actions(from_group):
    return [{
        'next_status': WAITING,
        "next_group": g['name'],
        "label": "Envoyer à " + g['name'],
        "rank": 1
    } for g in other_groups(from_group)]


# --------------------------------------------------------------------
# Secteurs, positions de contrôle et regroupement
SECTORS = [
    'A', 'B', 'C', 'D', 'E', 'F'
]

CWP = [
    'P1', 'P2', 'P3', 'P4', 'P5', 'P6'
]

UCESO = [
    'AB', 'ABC', 'CD', 'EF', 'CDEF'
]
