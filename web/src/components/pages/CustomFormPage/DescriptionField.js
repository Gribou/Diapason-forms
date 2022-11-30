import React from "react";
import { Box, Typography } from "@mui/material";

export default function DescriptionField({ label, helperText, sx }) {
  return (
    <Box sx={sx}>
      <Typography variant="subtitle2">{label}</Typography>
      {helperText && (
        <Typography
          variant="body2"
          fullWidth
          align="justify"
          sx={{ whiteSpace: "pre-wrap" }}
        >
          {helperText}
        </Typography>
      )}
    </Box>
  );
}
