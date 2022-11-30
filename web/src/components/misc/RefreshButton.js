import React from "react";
import { Tooltip, IconButton, CircularProgress } from "@mui/material";
import { Sync } from "mdi-material-ui";

export default function RefreshButton({
  refresh,
  loading,
  size = "24px",
  ...props
}) {
  return (
    <Tooltip title="Actualiser">
      <span>
        <IconButton
          color="primary"
          size="small"
          onClick={refresh}
          disabled={loading}
          {...props}
        >
          {loading ? <CircularProgress size={size} /> : <Sync />}
        </IconButton>
      </span>
    </Tooltip>
  );
}
