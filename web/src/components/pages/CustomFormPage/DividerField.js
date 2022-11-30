import React from "react";
import { Divider } from "@mui/material";

export default function DividerField({ sx = [], orientation }) {
  return (
    <Divider
      variant="fullWidth"
      flexItem
      sx={[{ flexGrow: 1 }, ...(Array.isArray(sx) ? sx : [sx])]}
      orientation={orientation}
    />
  );
}
