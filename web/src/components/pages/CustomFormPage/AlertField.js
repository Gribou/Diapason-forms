import React from "react";
import { Alert, AlertTitle } from "@mui/material";

export default function AlertField({
  label,
  helperText,
  sx = [],
  severity = "warning",
  ...props
}) {
  return (
    <Alert
      sx={[
        { flexGrow: 1, whiteSpace: "pre-wrap" },
        ...(Array.isArray(sx) ? sx : [sx]),
      ]}
      severity={severity}
      {...props}
    >
      <AlertTitle>{label}</AlertTitle>
      {helperText}
    </Alert>
  );
}
