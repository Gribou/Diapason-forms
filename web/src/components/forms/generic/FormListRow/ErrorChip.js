import React from "react";
import { Chip } from "@mui/material";
import { AlertDecagramOutline } from "mdi-material-ui";

export default function ErrorChip({ variant, ...props }) {
  return (
    <Chip
      icon={<AlertDecagramOutline />}
      size="small"
      sx={{ ml: 1 }}
      color="error"
      variant={variant}
      {...props}
    />
  );
}
