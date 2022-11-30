import React from "react";
import { Typography, Box } from "@mui/material";
import { Row, Cell, BooleanCell } from "components/misc/PageElements";
import { FLIGHT_PHASES } from "constants/fne";

export default function AircraftRowDisplay({
  callsign,
  is_origin,
  is_vfr,
  is_mil,
  advisory_type,
  contact_radio,
  ssr,
  flight_phase,
  assigned_fl,
  real_fl,
  index,
}) {
  const get_flight_phase_label = (flight_phase) =>
    FLIGHT_PHASES.find(({ value }) => value === flight_phase)?.label;

  return (
    <Row>
      <Cell span={12}>
        <Box
          border={1}
          borderRadius={5}
          borderColor="divider"
          mb={2}
          p={2}
          pt={1}
          sx={{ flexGrow: 1 }}
        >
          <Row>
            <Cell span={4}>
              <Typography variant="overline" color="textSecondary">{`Aéronef ${
                index + 1
              }`}</Typography>
            </Cell>
            <Cell span>
              <Typography variant="subtitle2">{`${callsign} (SSR ${
                ssr || "?"
              })`}</Typography>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                Phase de vol :
              </Typography>
              <Typography component="span" variant="body2">
                {get_flight_phase_label(flight_phase)}
              </Typography>
            </Cell>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                Niveau assigné :
              </Typography>
              <Typography component="span" variant="body2">
                {`FL ${assigned_fl || "0"}`}
              </Typography>
            </Cell>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                Niveau réel :
              </Typography>
              <Typography component="span" variant="body2">
                {`FL ${real_fl || "0"}`}
              </Typography>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                Type d&apos;avis :
              </Typography>
              <Typography component="span" variant="body2">
                {advisory_type}
              </Typography>
            </Cell>
            <BooleanCell
              label="A l'origine du signalement"
              value={is_origin}
              span={4}
            />
          </Row>
          <Row>
            <BooleanCell span label="Contact radio" value={contact_radio} />
            <BooleanCell span label="VFR" value={is_vfr} />
            <BooleanCell span label="Militaire" value={is_mil} />
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
