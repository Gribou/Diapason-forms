import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { PlaylistCheck } from "mdi-material-ui";
import { Link as RouterLink, useLocation } from "react-router-dom";
import { ROUTES } from "routes";

export default function BackToListButton() {
  const { search } = useLocation();
  return (
    <Tooltip title="Retour à la liste">
      <IconButton
        color="primary"
        size="small"
        component={RouterLink}
        to={{
          pathname: ROUTES.list.path,
          search,
        }}
      >
        <PlaylistCheck />
      </IconButton>
    </Tooltip>
  );
}
