import React, { Fragment } from "react";
import { Typography, Button } from "@mui/material";
import { LockOpen } from "mdi-material-ui";
import { Link as RouterLink } from "react-router-dom";
import { ROUTES } from "routes";
import ButtonBox from "./ButtonBox";

export default function AnonymousMenu() {
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
        connectez-vous pour accéder à la liste de fiches à traiter :
      </Typography>
      <ButtonBox>
        <Button
          size="large"
          variant="outlined"
          color="secondary"
          startIcon={<LockOpen />}
          component={RouterLink}
          to={ROUTES.login.path}
        >
          Connexion au compte utilisateur
        </Button>
      </ButtonBox>
    </Fragment>
  );
}
