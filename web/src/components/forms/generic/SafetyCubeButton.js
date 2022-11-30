import React from "react";
import { Button, Link, Tooltip } from "@mui/material";
import { purple } from "@mui/material/colors";
import { alpha } from "@mui/system";

import SafetyCubeIcon from "components/logos/SafetyCubeIcon";

export default function SafetyCubeButton({
  reference,
  url,
  status,
  sx = [],
  showRef,
  ...props
}) {
  return reference ? (
    <Tooltip title="SafetyCube">
      <Button
        startIcon={<SafetyCubeIcon />}
        {...props}
        size="small"
        component={Link}
        target="_blank"
        href={url}
        sx={[
          ...(Array.isArray(sx) ? sx : [sx]),
          {
            color: purple[700],
            "&:hover": {
              backgroundColor: (t) =>
                alpha(purple[700], t.palette.action.hoverOpacity),
              "@media (hover: none)": {
                backgroundColor: "transparent",
              },
            },
          },
        ]}
      >
        {(showRef ? reference : status) || "?"}
      </Button>
    </Tooltip>
  ) : null;
}
