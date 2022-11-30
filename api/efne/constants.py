from __future__ import unicode_literals

# --------------------------------------------------------------------
# Phases de vol
CLIMB = "CLIMB"
LEVEL = "LEVEL"
DESCENT = "DESCENT"
FLIGHT_PHASES = [(CLIMB, "Montée"), (LEVEL, "Croisière"),
                 (DESCENT, "Descente")]

# --------------------------------------------------------------------
# Type d'avis résolution TCAS
TA = "TA"
RA = "RA"
TCAS_TYPES = [(TA, 'Traffic Advisory'), (RA, "Resolution Advisory")]
