import React from "react";
import { Container, Typography, Stack, Box } from "@mui/material";
import AppIcon from "components/logos/AppIcon";

function ErrorPage({ title, children }) {
  return (
    <Container component="main" maxWidth="sm">
      <Stack sx={{ mt: 8 }}>
        <Box sx={{ alignSelf: "center" }}>
          <AppIcon size="large" />
        </Box>
        <Typography variant="h4" align="center" gutterBottom>
          {title}
        </Typography>
        {children}
      </Stack>
    </Container>
  );
}

export default function Error404() {
  return (
    <ErrorPage title="Page introuvable">
      <Typography variant="subtitle1" align="center">
        La page que vous cherchez n&apos;existe pas.
      </Typography>
    </ErrorPage>
  );
}
