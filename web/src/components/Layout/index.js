import React from "react";
import { Outlet } from "react-router-dom";
import { CssBaseline, AppBar, Stack, Toolbar, Box } from "@mui/material";
import { useSession } from "features/auth/hooks";
import Notifier from "./Notifier";
import CustomToolbar from "./Toolbar";
import GraphWarnings from "./GraphWarnings";

export default function Layout() {
  useSession();

  return (
    <Stack sx={{ minHeight: "100vh" }}>
      <CssBaseline />
      <AppBar position="fixed">
        <CustomToolbar />
      </AppBar>
      <Notifier style={{ top: 0, marginTop: 64 }} />
      <Toolbar />
      <GraphWarnings />
      <Box component="main" sx={{ flexGrow: 1 }}>
        <Outlet />
      </Box>
    </Stack>
  );
}
