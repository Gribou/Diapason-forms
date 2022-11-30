import React from "react";
import { Typography, Stack } from "@mui/material";

import { Cell } from "components/misc/PageElements";
import { PhotoDisplay } from "components/forms/fields";

export default function AircraftRow({ item, ...props }) {
  const { callsign, strip_url } = item;
  return (
    <Cell span={3} {...props}>
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="flex-end"
        sx={{
          flexGrow: 1,
          border: 1,
          borderRadius: 5,
          borderColor: "divider",
          mx: 1,
          my: 0,
          px: 2,
          py: 1,
        }}
      >
        <Typography variant="subtitle2" style={{ flexGrow: 1 }}>
          {callsign}
        </Typography>
        <PhotoDisplay url={strip_url} />
      </Stack>
    </Cell>
  );
}
