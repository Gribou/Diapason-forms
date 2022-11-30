import React from "react";
import { Paper, Box, Stack, Typography } from "@mui/material";

export default function Part({ children, title }) {
  return (
    <Paper
      sx={{
        mb: 2,
        p: 2,
        height: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {title && (
        <Box
          sx={{
            mb: 2,
            minHeight: "48px",
            alignItems: "center",
            display: "flex",
          }}
        >
          <Typography component="h2" variant="h6">
            {title}
          </Typography>
        </Box>
      )}
      <Stack spacing={1} sx={{ flexGrow: 1 }}>
        {children}
      </Stack>
    </Paper>
  );
}
