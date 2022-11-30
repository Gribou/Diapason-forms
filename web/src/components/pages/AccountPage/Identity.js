import React from "react";
import { Stack, Typography } from "@mui/material";
import Part from "./Part";

export default function Identity({ username, email, groups, is_sso }) {
  return (
    <Part title={`Identité${is_sso ? " (Angélique)" : ""}`}>
      <Stack direction="row" alignItems="center">
        <Typography
          component="span"
          variant="subtitle2"
          sx={{ width: "120px" }}
        >
          Nom d&apos;utilisateur :
        </Typography>
        <Typography component="span" variant="body2">
          {username}
        </Typography>
      </Stack>
      <Stack direction="row" alignItems="center">
        <Typography
          component="span"
          variant="subtitle2"
          sx={{ width: "120px" }}
        >
          Adresse e-mail :
        </Typography>
        <Typography component="span" variant="body2" noWrap>
          {email}
        </Typography>
      </Stack>
      <Stack direction="row" alignItems="center" sx={{ pb: 1 }}>
        <Typography
          component="span"
          variant="subtitle2"
          sx={{ width: "120px" }}
        >
          Groupes:
        </Typography>
        <Typography component="span" variant="body2">
          {groups?.map(({ name }) => name)?.join(", ") || "Aucun"}
        </Typography>
      </Stack>
    </Part>
  );
}
