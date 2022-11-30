import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { ChevronLeft } from "mdi-material-ui";
import { Link as RouterLink, useLocation } from "react-router-dom";

export default function PreviousButton({ uuid, route }) {
  const { search } = useLocation();
  return (
    <Tooltip title="Fiche précédente">
      <IconButton
        color="primary"
        size="small"
        component={RouterLink}
        to={{
          pathname: route?.path?.replace(":pk", uuid),
          search,
        }}
      >
        <ChevronLeft />
      </IconButton>
    </Tooltip>
  );
}
