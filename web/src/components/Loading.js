import React from "react";
import {
  Stack,
  CssBaseline,
  Toolbar,
  AppBar,
  Box,
  Typography,
  CircularProgress,
} from "@mui/material";
import { DEBUG } from "constants/config";

export default function Loading() {
  return (
    <Stack sx={{ minHeight: "100vh" }}>
      <CssBaseline />
      <AppBar>
        <Toolbar>
          <Typography variant="h5" color="inherit" noWrap>{`eFNE${
            DEBUG ? " Debug" : ""
          }`}</Typography>
        </Toolbar>
      </AppBar>
      <Toolbar />
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          justifyContent: "auto",
          alignItems: "center",
        }}
      >
        <CircularProgress sx={{ mx: "auto" }} size={60} />
      </Box>
    </Stack>
  );
}
