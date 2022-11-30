import React from "react";
import { Stack, Typography } from "@mui/material";
import {
  CheckboxMarkedCircleOutline,
  CloseCircleOutline,
} from "mdi-material-ui";
import Part from "./Part";

function RoleTypo({ enabled, children, ...props }) {
  return (
    <Stack direction="row" alignItems="center" {...props}>
      {enabled ? (
        <CheckboxMarkedCircleOutline color="success" />
      ) : (
        <CloseCircleOutline color="error" />
      )}
      <Typography
        component="span"
        variant="body2"
        align="justify"
        sx={{
          ml: 2,
          textDecorationLine: enabled ? "none" : "line-through",
          textDecorationColor: "inherit",
          color: enabled ? "inherit" : "text.disabled",
        }}
      >
        {children}
      </Typography>
    </Stack>
  );
}

export default function Roles({
  is_validator,
  is_investigator,
  has_all_access,
}) {
  return (
    <Part title="Roles">
      <RoleTypo enabled={is_validator}>
        Je peux valider les nouvelles fiches
      </RoleTypo>
      <RoleTypo enabled={is_investigator}>
        Je peux analyser et traiter les fiches qui me sont attribuées
      </RoleTypo>
      <RoleTypo enabled={has_all_access} sx={{ pb: 1 }}>
        Je peux consulter toutes les fiches en cours de traitement
      </RoleTypo>
    </Part>
  );
}
