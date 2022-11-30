import React from "react";
import { Typography, Box } from "@mui/material";

import { Row, Cell } from "components/misc/PageElements";
import { PhotoDisplay } from "components/forms/fields";

export default function AircraftRow({ item, index, ...props }) {
  const {
    callsign,
    ssr,
    type,
    provenance,
    destination,
    fl,
    position,
    strip_url,
  } = item;
  return (
    <Row key={index} {...props}>
      <Cell span={12} {...props}>
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
            <Cell span={4}>
              <Typography variant="overline" color="textSecondary">{`Aéronef ${
                (index || 0) + 1
              }`}</Typography>
            </Cell>
            <Cell span>
              <Typography variant="subtitle2" display="inline">
                {`${callsign} (SSR ${ssr || "?"})`}
              </Typography>
            </Cell>
           <Cell>
                <PhotoDisplay url={strip_url} />
              </Cell>
          </Row>
          <Row>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                {"Type d'aéronef : "}
              </Typography>
              <Typography component="span" variant="body2">
                {type || "?"}
              </Typography>
            </Cell>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                {"Provenance : "}
              </Typography>
              <Typography component="span" variant="body2">
                {provenance || "?"}
              </Typography>
            </Cell>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                {"Destination : "}
              </Typography>
              <Typography component="span" variant="body2">
                {destination || "?"}
              </Typography>
            </Cell>
          </Row>
          <Row>
            <Cell span={4}>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                {"FL : "}
              </Typography>
              <Typography component="span" variant="body2">
                {fl || "?"}
              </Typography>
            </Cell>
            <Cell span>
              <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
                {"Position : "}
              </Typography>
              <Typography component="span" variant="body2">
                {position || "?"}
              </Typography>
            </Cell>
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
