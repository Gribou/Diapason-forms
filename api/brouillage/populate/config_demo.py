from shared.populate import config_demo as shared_config


INTERFERENCE_TYPES = [
    {"name": "Autre fréquence ATC"},
    {"name": "Paroles/Musique"},
    {"name": "Bruit blanc/porteuse"},
    {"name": "Emission permanente"},
    {"name": "Battements/Bruit industriel"},
    {"name": "Autre"}, {"name": "Rien"}
]

# Draft -> CDS -> ETU -> DONE
BROUILLAGE_GRAPH = {
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
        shared_config.ETU: [{
            'next_status': shared_config.IN_PROGRESS,
            'next_group': shared_config.ETU,
            'label': 'Marquer comme "en cours"',
            'is_default': True,
        }, {
            "next_status": shared_config.DONE,
            "next_group": shared_config.ETU,
            "label": 'Marquer comme "traité"'
        }],
    },
    shared_config.IN_PROGRESS: {
        shared_config.ETU: [{
            "next_status": shared_config.DONE,
            "next_group": shared_config.ETU,
            "label": 'Marquer comme "traité"',
            'is_default': True
        }, {
            'next_status': shared_config.WAITING,
            'next_group': shared_config.ETU,
            'label': 'Marquer comme "en cours"',
        }]
    },
    shared_config.DONE: {
        shared_config.CDS: [{
            'next_status': shared_config.WAITING,
            'next_group': shared_config.ETU,
            'label': 'Envoyer à ' + shared_config.ETU,
            'is_default': True
        }, {
            'next_status': shared_config.WAITING,
            'next_group': shared_config.CDS,
            'label': 'Marquer comme "en attente"',
        }, {
            'next_status': shared_config.TO_BE_DELETED,
            'next_group': shared_config.CDS,
            'label': 'Marquer comme "à supprimer"',
            "is_terminal": True
        }],
        shared_config.ETU: [{
            "next_status": shared_config.TO_BE_DELETED,
            "label": 'Marquer comme "répondu"',
            'is_default': True,
            'is_terminal': True
        }, {
            "next_status": shared_config.WAITING,
            "label": "Marquer comme 'en attente'",
            "next_group": shared_config.ETU
        }]
    }
}
