import React from "react";
import { Box, Typography } from "@mui/material";
import { Row, Cell, LabelCell, ValueCell } from "components/misc/PageElements";
import { PhotoDisplay } from "components/forms/fields";

export default function AircraftRow({ item, index, ...props }) {
  const { callsign, strip_url, fl, waypoint, distance, bearing, plaintiff } =
    item;
  return (
    <Row key={index} {...props}>
      <Cell span={6} {...props}>
        <Box
          sx={{
            border: 1,
            borderRadius: 5,
            borderColor: "divider",
            mx: 1,
            mb: 2,
            mt: 0,
            p: 2,
            pt: 1,
            flexGrow: 1,
          }}
        >
          <Row alignItems="center">
            <Cell span={3}>
              <Typography variant="overline" color="textSecondary">{`Aéronef ${
                (index || 0) + 1
              }`}</Typography>
            </Cell>
            <Cell span>
              <Typography variant="subtitle2" display="inline">
                {callsign}
              </Typography>
            </Cell>
            <Cell>
              <PhotoDisplay url={strip_url} />
            </Cell>
          </Row>
          <Row>
            <LabelCell label="Position" span={false} />
            <ValueCell
              value={`${waypoint || "?"} - ${distance || "?"} NM - ${
                bearing || "?"
              }° - FL ${fl || "?"}`}
            />
          </Row>
          <Row>
            <LabelCell label="Reçu par" span={false} />
            <ValueCell value={plaintiff} />
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
