import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Button, Typography, Divider, Stack } from "@mui/material";
import { Plus } from "mdi-material-ui";
import ButtonBox from "./ButtonBox";
import { getRouteForNewForm } from "routes";

const make_form_button = (form, highlight, key) => (
  <Button
    key={key}
    size="large"
    variant={highlight ? "contained" : "outlined"}
    color="primary"
    startIcon={<Plus />}
    component={RouterLink}
    to={getRouteForNewForm(form)}
  >
    {form?.title}
  </Button>
);

export default function FormListMenu({ forms, label, divider }) {
  return (
    <Stack sx={{ maxWidth: "sm", mx: "auto" }}>
      {label && (
        <Typography
          variant="button"
          color="textSecondary"
          align="center"
          sx={{ width: "100%", display: "block" }}
          gutterBottom
        >
          {label}
        </Typography>
      )}
      <ButtonBox>
        {forms?.map((form, i) => make_form_button(form, form?.is_fne, i))}
      </ButtonBox>
      {divider && <Divider flexItem sx={{ my: 2 }} />}
    </Stack>
  );
}
