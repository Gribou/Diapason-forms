import React from "react";
import { Navigate } from "react-router-dom";
import { Grid, Typography, Alert } from "@mui/material";
import { useAuthenticated, useMe } from "features/auth/hooks";
import { useAdminEmail } from "features/config/hooks";
import { ROUTES } from "routes";

import Identity from "./Identity";
import Roles from "./Roles";
import Notifications from "./Notifications";

export default function AccountPage() {
  const is_authenticated = useAuthenticated();
  const email_admin = useAdminEmail();
  const me = useMe();

  const relevant_forms = me?.form_relevance
    ? Object.entries(me?.form_relevance)
        ?.filter(([, is_relevant]) => is_relevant)
        ?.map(([key]) => key)
    : [];

  return !is_authenticated ? (
    <Navigate to={ROUTES.login.path} />
  ) : (
    <Grid
      container
      sx={{
        maxWidth: "md",
        mx: "auto",
        p: { xs: 1, md: 3 },
      }}
    >
      <Grid item xs={12} sx={{ px: 1 }}>
        <Typography component="h2" variant="h4" color="primary" sx={{ py: 2 }}>
          Mon compte
        </Typography>
      </Grid>
      <Grid item xs={12} sx={{ p: 1 }}>
        <Alert severity="info">
          {
            "Si les groupes auxquels vous appartenez ou les rôles qui vous sont attribués ne correspondent pas à vos fonctions, contactez l'administrateur "
          }
          {email_admin ? `(${email_admin}) ` : ""}
          {"pour les mettre à jour."}
        </Alert>
      </Grid>
      <Grid item xs={12} sm={6} sx={{ p: 1 }}>
        <Identity {...me} />
      </Grid>
      <Grid item xs={12} sm={6} sx={{ p: 1 }}>
        <Roles {...me} />
      </Grid>
      {relevant_forms?.length > 0 && (
        <Grid item sx={{ p: 1 }}>
          <Notifications {...me} relevant_forms={relevant_forms} />
        </Grid>
      )}
    </Grid>
  );
}
