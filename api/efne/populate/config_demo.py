from shared.populate import config_demo as shared_config

# -------------------------------------------------------------------
# Type d'évènement
EVENTS = [
    {
        "name": "Contrôle"
    },
    {
        "name": "TCAS",
        'is_tcas': True
    },
    {
        "name": "ATFM",
    },
    {
        "name": "Coflight"
    },
    {
        "name": "JHMI"
    },
    {
        "name": "Téléphonie"
    },
    {
        "name": "Radio"
    },
    {
        "name": "Avis ou suggestion"
    },
    {
        "name": "Autre"
    },
]

TECH_ACTIONS = [{
    "name": "Vidage STR - via la MO",
    "helperText": "Historique de la piste dans le STR"
}, {
    "name": "ODSARCH - via la MO",
    "helperText": "Archivage ODS de la position via la MO"
}]

TECH_EVENTS = [{
    "name": "STCA",
    "helperText": "Problème de déclenchement du filet de sauvegarde"
}, {
    "name": "TCAS",
}, {
    "name": "HN",
}, {
    "name": "Datalink",
}]

# --------------------------------------------------------------------
# Types de rédacteurs
REDAC_TYPES = ["PCR", "PCO", "ECR", "ECO", "CDS", "ACDS", "QSS"]

# --------------------------------------------------------------------
# Graph d'actions pour Fne

# DRAFT -> CDS -> QSE -> ... any subs ... -> QSE -> DONE
FNE_GRAPH = {
    '': {
        '': [{
            # send to CDS for validation
            'next_status': shared_config.WAITING,
            'next_group': shared_config.CDS,
            'label': 'Envoyer à ' + shared_config.CDS,
            'is_default': True
        }]
    },
    shared_config.DRAFT: {
        '': [{
            # send to CDS for validation
            'next_status': shared_config.WAITING,
            'next_group': shared_config.CDS,
            'label': 'Envoyer à ' + shared_config.CDS,
            'is_default': True
        }]
    },
    shared_config.WAITING: {
        shared_config.CDS: [{
            'next_status': shared_config.DONE,
            'next_group': shared_config.CDS,
            'label': 'Marquer comme "validé"',
            'is_default': True
        }, {
            'next_status': shared_config.TO_BE_DELETED,
            'next_group': shared_config.CDS,
            'label': 'Marquer comme "à supprimer"',
            'is_terminal': True
        }],
        shared_config.QSE: [{
            'next_status': shared_config.IN_PROGRESS,
            'next_group': shared_config.QSE,
            'label': 'Marquer comme "en cours"',
        }, {
            "next_status": shared_config.DONE,
            "next_group": shared_config.QSE,
            "label": 'Marquer comme "traité"'
        }] + shared_config.make_transfer_actions(shared_config.QSE),
        shared_config.QSA: [{
            'next_status': shared_config.IN_PROGRESS,
            'next_group': shared_config.QSA,
            'label': 'Marquer comme "en cours"',
        }, {
            "next_status": shared_config.DONE,
            "next_group": shared_config.QSE,
            "label": 'Marquer comme "traité"',
        }] + shared_config.make_transfer_actions(shared_config.QSA),
        shared_config.ETU: [{
            'next_status': shared_config.IN_PROGRESS,
            'next_group': shared_config.ETU,
            'label': 'Marquer comme "en cours"',
        }, {
            "next_status": shared_config.DONE,
            "next_group": shared_config.QSE,
            "label": 'Marquer comme "traité"',
        }] + shared_config.make_transfer_actions(shared_config.ETU),
    },
    shared_config.IN_PROGRESS: {
        # current group can send to QSE for closure or transfer to another
        # group
        current_group['name']: [{
            "next_status": shared_config.DONE,
            "next_group": shared_config.QSE,
            "label": 'Marquer comme "traité"',
        }, {
            "next_status": shared_config.WAITING,
            "next_group": current_group['name'],
            "label": 'Marquer comme "en attente"',
        }] + [{
            "next_status": shared_config.WAITING,
            "next_group": g['name'],
            "label": "Envoyer à " + g['name'],
        } for g in shared_config.other_groups(current_group['name'])]
        for current_group in shared_config.NOT_VALIDATOR_GROUPS
    },
    shared_config.DONE: {
        # DONE fnes are sent to QSE
        shared_config.CDS: [{
            'next_status': shared_config.WAITING,
            'next_group': shared_config.QSE,
            'label': 'Envoyer à ' + shared_config.QSE,
            'is_default': True
        }, {
            'next_status': shared_config.TO_BE_DELETED,
            'next_group': shared_config.CDS,
            'label': 'Marquer comme "à supprimer"',
            'is_terminal': True
        }],
        # DONE fnes are deleted after treatment by QSE
        shared_config.QSE: [{
            "next_status": shared_config.TO_BE_DELETED,
            "label": 'Marquer comme "répondu"',
            'is_default': True,
            'is_terminal': True
        }, {
            "next_status": shared_config.IN_PROGRESS,
            "label": "Marquer comme 'en cours'",
            "next_group": shared_config.QSE
        }, {
            "next_status": shared_config.WAITING,
            "label": "Marquer comme 'en attente'",
            "next_group": shared_config.QSE
        }]
    },
}
