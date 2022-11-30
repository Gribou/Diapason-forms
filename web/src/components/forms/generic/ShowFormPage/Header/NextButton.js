import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { ChevronRight } from "mdi-material-ui";
import { Link as RouterLink, useLocation } from "react-router-dom";

export default function NextButton({ uuid, route }) {
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
        <ChevronRight />
      </IconButton>
    </Tooltip>
  );
}
