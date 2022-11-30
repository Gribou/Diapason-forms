import React from "react";
import { Chip, CircularProgress } from "@mui/material";

export default function NormalChip({ IconComponent, loading, ...props }) {
  return (
    <Chip
      icon={loading ? <CircularProgress size={12} /> : <IconComponent />}
      size="small"
      sx={{ ml: 1 }}
      {...props}
    />
  );
}
