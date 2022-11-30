import React from "react";
import { Container, Stack, Typography, Paper } from "@mui/material";

import AppIcon from "components/logos/AppIcon";

export default function AuthPage({ loading, title, children }) {
  return (
    <Container component="main" maxWidth="sm">
      <Paper>
        <Stack
          alignItems="center"
          sx={{
            mt: { xs: 2, md: 4 },
            p: 2,
          }}
        >
          <AppIcon size="large" loading={loading} />
          <Typography component="h1" variant="h5">
            {title}
          </Typography>
          {children}
        </Stack>
      </Paper>
    </Container>
  );
}
