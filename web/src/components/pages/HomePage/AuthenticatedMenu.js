import React, { Fragment } from "react";
import { Typography, Button, Badge } from "@mui/material";
import { PlaylistCheck } from "mdi-material-ui";
import { Link as RouterLink } from "react-router-dom";
import { ROUTES } from "routes";
import ButtonBox from "./ButtonBox";

export default function AnonymousMenu({ count }) {
  return (
    <Fragment>
      <Typography
        variant="h6"
        color="textSecondary"
        align="center"
        paragraph
        sx={{ mt: 6 }}
      >
        Si vous êtes Chef de Salle ou si vous appartenez à un subdivision,
        <br />
        cliquez-ci dessous pour accéder à la liste de fiches à traiter :
      </Typography>
      <ButtonBox>
        <Button
          size="large"
          variant="outlined"
          color="secondary"
          startIcon={<PlaylistCheck />}
          component={RouterLink}
          to={ROUTES.list.path}
        >
          <Badge badgeContent={count} color="error">
            Liste des fiches à traiter
          </Badge>
        </Button>
      </ButtonBox>
    </Fragment>
  );
}
