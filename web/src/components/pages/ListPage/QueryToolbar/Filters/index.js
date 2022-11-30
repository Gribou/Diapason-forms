import React, { Fragment } from "react";
import { Button } from "@mui/material";
import { MenuDown, Filter } from "mdi-material-ui";
import useFiltersMenu from "./FiltersMenu";

export default function Filters({ meta }) {
  const menu = useFiltersMenu(meta);

  return (
    <Fragment>
      <Button
        color="primary"
        size="small"
        sx={{ whiteSpace: "nowrap" }}
        variant="outlined"
        endIcon={<MenuDown />}
        startIcon={<Filter />}
        onClick={menu.open}
      >
        Filtrer
      </Button>
      {menu.display}
    </Fragment>
  );
}
