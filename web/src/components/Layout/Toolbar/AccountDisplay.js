import React, { Fragment } from "react";
import { Link, IconButton } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { AccountCircle } from "mdi-material-ui";
import { useMe } from "features/auth/hooks";
import { ROUTES } from "routes";

export default function AccountDisplay(props) {
  const { username } = useMe();
  return (
    <Fragment>
      <IconButton
        component={RouterLink}
        to={ROUTES.account.path}
        color="inherit"
      >
        <AccountCircle />
      </IconButton>
      <Link
        component={RouterLink}
        to={ROUTES.account.path}
        color="inherit"
        variant="subtitle2"
        underline="hover"
        {...props}
      >
        {username}
      </Link>
    </Fragment>
  );
}
