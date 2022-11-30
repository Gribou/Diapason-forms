import React from "react";
import { Chip } from "@mui/material";

export function WarningBadge({ content, ...props }) {
  return (
    <Chip
      size="small"
      label={content}
      sx={{ ml: -1, bgcolor: "warning.main", color: "common.white" }}
      {...props}
    />
  );
}

export function AlarmBadge({ content, ...props }) {
  return (
    <Chip
      size="small"
      label={content}
      sx={{ ml: -1, bgcolor: "error.main", color: "common.white" }}
      {...props}
    />
  );
}
