import React from "react";
import {
  Link,
  Toolbar,
  Button,
  IconButton,
  Tooltip,
  Badge,
  Box,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { Link as RouterLink } from "react-router-dom";
import { PlaylistCheck, Poll, Home } from "mdi-material-ui";

import { DEBUG, UPDATE_PROFILE_PERIOD } from "constants/config";
import { useAuthenticated } from "features/auth/hooks";
import {
  useFeatures,
  useToolbarMenu,
  useAssignedCount,
  useVersion,
} from "features/config/hooks";
import { ROUTES } from "routes";
import EFNEIcon from "components/logos/EFNEIcon";

import LogoutButton from "./LogoutButton";
import FormButton from "./FormButton";
import AccountDisplay from "./AccountDisplay";

export default function MyToolbar() {
  const theme = useTheme();
  const is_authenticated = useAuthenticated();
  const assigned_count = useAssignedCount({
    pollingInterval: UPDATE_PROFILE_PERIOD,
  });
  const version = useVersion();
  const { show_stats } = useFeatures();
  const form_categories = useToolbarMenu();

  const logo = (
    <Tooltip title={version || "version ?"}>
      <IconButton
        component={RouterLink}
        to={ROUTES.home.path}
        edge="start"
        color="inherit"
      >
        <EFNEIcon
          fontSize="large"
          baseColor={theme.palette.common.white}
          accentColor={theme.palette.common.white}
        />
      </IconButton>
    </Tooltip>
  );
  const app_display = (
    <Link
      component={RouterLink}
      to={ROUTES.home.path}
      sx={{ mr: { xs: 1, md: 4 }, display: { xs: "none", sm: "block" } }}
      variant="h5"
      underline="hover"
      color="inherit"
      noWrap
    >{`eFNE${DEBUG ? " Debug" : ""}`}</Link>
  );

  const account_display = is_authenticated && <AccountDisplay sx={{ mr: 2 }} />;

  const home_button = (
    <Tooltip title="Page d'accueil">
      <IconButton component={RouterLink} to={ROUTES.home.path} color="inherit">
        <Home />
      </IconButton>
    </Tooltip>
  );

  const new_button = form_categories?.map(({ forms }, i) => (
    <FormButton key={i} forms={forms} sx={{ mr: 1 }} />
  ));

  const list_button = is_authenticated && (
    <Button
      size="small"
      color="inherit"
      variant="outlined"
      component={RouterLink}
      to={ROUTES.list.path}
      startIcon={
        <Badge
          badgeContent={assigned_count}
          color="error"
          anchorOrigin={{
            vertical: "top",
            horizontal: "left",
          }}
        >
          <PlaylistCheck />
        </Badge>
      }
      sx={{ mr: 2, whiteSpace: "nowrap" }}
    >
      à traiter
    </Button>
  );

  const stats_button = show_stats && (
    <Tooltip title="Statistiques d'utilisation d'eFNE">
      <IconButton
        component={RouterLink}
        to={ROUTES.stats.path}
        color="inherit"
        sx={{ mr: 2 }}
      >
        <Poll />
      </IconButton>
    </Tooltip>
  );

  const login_button = !is_authenticated && (
    <Button
      variant="outlined"
      size="small"
      color="inherit"
      component={RouterLink}
      to={ROUTES.login.path}
      edge="end"
    >
      Connexion
    </Button>
  );

  const logout_button = is_authenticated && <LogoutButton />;

  return (
    <Toolbar>
      {logo}
      {app_display}
      {home_button}
      {new_button}
      {list_button}
      <Box sx={{ flexGrow: 1 }} />
      {stats_button}
      {account_display}
      {logout_button}
      {login_button}
    </Toolbar>
  );
}
