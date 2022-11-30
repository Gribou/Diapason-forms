import React, { Fragment } from "react";
import { Container, Typography, Divider, Box, Stack } from "@mui/material";
import EFNEIcon from "components/logos/EFNEIcon";
import { useAuthenticated, useMe } from "features/auth/hooks";
import { useFormsMenu } from "features/config/hooks";
import FormListMenu from "./FormListMenu";
import AnonymousMenu from "./AnonymousMenu";
import AuthenticatedMenu from "./AuthenticatedMenu";

export default function HomePage() {
  const is_authenticated = useAuthenticated();
  const { assigned_forms_count } = useMe();
  const categories = useFormsMenu();
  return (
    <Fragment>
      <Box sx={{ bgcolor: "background.paper", py: 2 }}>
        <Stack
          sx={{ maxWidth: "md", mx: "auto" }}
          direction="row"
          alignItems="center"
          justifyContent="center"
        >
          <EFNEIcon sx={{ width: "4em", height: "4em", m: 2 }} />
          <Typography
            component="h1"
            variant="h2"
            color="textPrimary"
            gutterBottom
            sx={{ mx: 2, mb: 0 }}
          >
            Bienvenue sur eFNE
          </Typography>
        </Stack>
      </Box>
      <Divider />
      <Container maxWidth="md" sx={{ py: 2 }}>
        {categories && (
          <Typography
            variant="h6"
            color="textSecondary"
            align="center"
            paragraph
            sx={{ mt: 6 }}
          >
            Cliquez sur les boutons ci-dessous pour commencer une nouvelle fiche
            :
          </Typography>
        )}
        {categories?.map(({ label, ...category }, i) => (
          <FormListMenu
            key={i}
            {...category}
            divider={i < categories?.length - 1}
            label={categories?.length > 1 && label}
          />
        ))}
        {!is_authenticated ? (
          <AnonymousMenu />
        ) : (
          <AuthenticatedMenu count={assigned_forms_count} />
        )}
      </Container>
    </Fragment>
  );
}
