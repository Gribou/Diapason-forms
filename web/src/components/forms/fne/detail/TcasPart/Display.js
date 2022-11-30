import React from "react";
import { Typography } from "@mui/material";
import AircraftDisplay from "./AircraftRowDisplay";

import {
  Part,
  Row,
  Cell,
  BooleanCell,
  DividerRow,
} from "components/misc/PageElements";

export default function Display({ data, ...props }) {
  const { tcas_report: tcasReport } = data;

  return (
    <Part title="Compte-rendu d'évènement TCAS" defaultExpanded {...props}>
      {tcasReport?.aircrafts?.map((aircraft, i) => (
        <AircraftDisplay key={i} index={i} {...aircraft} />
      ))}

      <Row>
        <Cell span={4}>
          <Typography variant="overline">Analyse pilote</Typography>
        </Cell>
        <Cell span>
          <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
            Distance minimale :
          </Typography>
          <Typography component="span" variant="body2">
            {tcasReport?.pilote_min_distance !== undefined
              ? `${tcasReport?.pilote_min_distance} NM`
              : "?"}
          </Typography>
        </Cell>
        <Cell span>
          <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
            Altitude minimale :
          </Typography>
          <Typography component="span" variant="body2">
            {tcasReport?.pilote_min_altitude !== undefined
              ? `${tcasReport?.pilote_min_altitude} ft`
              : "?"}
          </Typography>
        </Cell>
      </Row>
      <Row>
        <Cell span={4}>
          <Typography variant="overline">Analyse contrôleur</Typography>
        </Cell>
        <Cell span>
          <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
            Distance minimale :
          </Typography>
          <Typography component="span" variant="body2">
            {tcasReport?.ctl_min_distance !== undefined
              ? `${tcasReport?.ctl_min_distance} NM`
              : "?"}
          </Typography>
        </Cell>
        <Cell span>
          <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
            Altitude minimale :
          </Typography>
          <Typography component="span" variant="body2">
            {tcasReport?.ctl_min_altitude !== undefined
              ? `${tcasReport?.ctl_min_altitude} ft`
              : "?"}
          </Typography>
        </Cell>
      </Row>
      <DividerRow />
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="Y a-t-il eu une information de trafic ?"
          value={tcasReport?.traffic_info}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="Sur demande du pilote ?"
          value={tcasReport?.pilot_request}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="Si OUI, la demande a-t-elle été faite avant ou après la
                          manoeuvre ?"
          yesLabel="Avant"
          noLabel="Après"
          value={tcasReport?.before_manoeuvre}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="A votre avis, l'action du pilote était-elle
                          justifiée ?"
          value={tcasReport?.pilot_action_required}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="Cet évènement a-t-il perturbé votre gestion du trafic ?"
          value={tcasReport?.disrupted_traffic}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="L'un des pilotes a-t-il signalé vouloir rédiger un
                          ASR ?"
          value={tcasReport?.asr}
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          noColon
          span
          label="Le filet de sauvegarde s'est-il déclenché ?"
          value={tcasReport?.safety_net}
        />
      </Row>
    </Part>
  );
}
