import React from "react";
import { Chip } from "@mui/material";
import { AlertOutline } from "mdi-material-ui";

export default function WarningChip({ variant, ...props }) {
  return (
    <Chip
      icon={<AlertOutline />}
      color="warning"
      sx={{ ml: 1 }}
      size="small"
      variant={variant}
      {...props}
    />
  );
}
