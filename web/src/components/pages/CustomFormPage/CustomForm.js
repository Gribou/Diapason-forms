import React from "react";
import {
  Grid,
  Button,
  Accordion,
  AccordionDetails,
  Typography,
  Box,
} from "@mui/material";
import { Row, Cell } from "components/misc/PageElements";
import {
  FormCheckboxField,
  FormCheckboxGroupField,
  FormDateTimeField,
  FormDateField,
  FormTimeField,
  FormPasswordField,
  FormRadioField,
  FormSelectField,
  FormTextField,
  PhotoField,
  DrawingField,
} from "components/forms/fields";
import DescriptionField from "./DescriptionField";
import DividerField from "./DividerField";
import EmptyField from "./EmptyField";
import ButtonGroupField from "./ButtonGroupField";
import ButtonField from "./ButtonField";
import AlertField from "./AlertField";

const COMPONENT_MAP = {
  "text-input": FormTextField,
  password: FormPasswordField,
  checkbox: FormCheckboxField,
  "checkbox-group": FormCheckboxGroupField,
  radio: FormRadioField,
  button: ButtonField,
  "button-group": ButtonGroupField,
  select: FormSelectField,
  date: FormDateField,
  time: FormTimeField,
  datetime: FormDateTimeField,
  photo: PhotoField,
  drawing: DrawingField,
  alert: AlertField,
  text: DescriptionField,
  divider: DividerField,
  empty: EmptyField,
};

function CustomField({
  type,
  label,
  slug,
  help_text,
  choices,
  attrs,
  required,
  formProps,
  sx,
}) {
  const Field = COMPONENT_MAP[type] || DescriptionField;
  const adapted_choices =
    type === "radio"
      ? choices?.map((c) => ({ label: c, value: c }))
      : type === "checkbox-group"
      ? choices?.map((c) => ({ name: c, pk: c }))
      : choices;
  return (
    <Field
      id={slug}
      label={label}
      helperText={help_text}
      choices={adapted_choices}
      required={required}
      {...attrs}
      {...formProps}
      sx={sx}
    />
  );
}

export default function CustomForm({
  fields,
  form_props,
  description,
  disabled,
  handleSubmit,
}) {
  const rows = [...new Set(fields?.map(({ row }) => row))];

  return (
    <Box
      component="form"
      noValidate
      onSubmit={handleSubmit}
      sx={{ width: "100%", mt: 1 }}
    >
      <Accordion>
        <AccordionDetails>
          <Grid container>
            {description && (
              <Row>
                <Cell span>
                  <Typography variant="body2" sx={{ my: 1 }}>
                    {description}
                  </Typography>
                </Cell>
              </Row>
            )}
            {rows?.map((row, i) => (
              <Row key={i}>
                {fields
                  ?.filter((field) => field?.row === row)
                  ?.map((field, j) => (
                    <Cell
                      key={j}
                      span={field?.size === 0 ? false : field?.size || true}
                    >
                      <CustomField
                        {...field}
                        formProps={form_props}
                        sx={{ my: 1 }}
                      />
                    </Cell>
                  ))}
              </Row>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>
      <Grid xs item>
        <Button
          fullWidth
          variant="contained"
          color="primary"
          type="submit"
          disabled={disabled}
          sx={{ my: 2 }}
        >
          Valider
        </Button>
      </Grid>
    </Box>
  );
}
