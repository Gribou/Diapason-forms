import React, { Fragment, useRef } from "react";
import { Button, ButtonGroup } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { Plus, MenuDown } from "mdi-material-ui";
import { getRouteForNewForm } from "routes";
import useNewFormMenu from "./NewFormMenu";

function MainFormButton({ form, sx = [] }) {
  return (
    <Button
      component={RouterLink}
      to={getRouteForNewForm(form)}
      startIcon={<Plus />}
      size="small"
      variant="contained"
      color="inherit"
      sx={[{ color: "primary.dark" }, ...(Array.isArray(sx) ? sx : [sx])]}
    >
      {form.title}
    </Button>
  );
}

export default function FormButton({ forms = [], sx = [] }) {
  const menuAnchorRef = useRef();
  const new_form_menu = useNewFormMenu(menuAnchorRef, forms?.slice(1));
  const main_form = forms?.[0] || {};

  const single_button = <MainFormButton form={main_form} sx={sx} />;

  const group_button = (
    <Fragment>
      <ButtonGroup
        size="small"
        variant="contained"
        color="inherit"
        sx={[{ color: "primary.dark" }, ...(Array.isArray(sx) ? sx : [sx])]}
        ref={menuAnchorRef}
      >
        <MainFormButton
          form={main_form}
          sx={{
            borderBottomRightRadius: 0,
            borderTopRightRadius: 0,
            borderRight: 1,
            borderRightColor: "primary.dark",
            whiteSpace: "nowrap",
          }}
        />
        <Button
          sx={{
            borderBottomLeftRadius: 0,
            borderTopLeftRadius: 0,
          }}
          onClick={new_form_menu.open}
        >
          <MenuDown />
        </Button>
      </ButtonGroup>
      {new_form_menu.display}
    </Fragment>
  );

  return forms?.length > 1 ? group_button : single_button;
}
