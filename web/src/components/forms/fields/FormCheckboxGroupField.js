import React, { Fragment } from "react";
import {
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  FormHelperText,
  Checkbox,
} from "@mui/material";

export default function FormCheckboxGroupField({
  id,
  values,
  errors,
  touched,
  label,
  onChange,
  choices,
  column,
  getOptionLabel = (choice) => choice?.name,
  getOptionValue = (choice) => choice?.pk?.toString(),
  getOptionHelperText = () => undefined,
  getOptionSelected = (choice, value) =>
    Boolean(value?.find(({ pk }) => pk === choice?.pk)),
  helperText,
  ...props
}) {
  const get_error_text = () => {
    const error = errors[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  const get_group_value = () => values?.[id] || [];

  const handleChange = (event) => {
    // exclude this choice from current values (to avoid duplicates)
    const new_value = [
      ...get_group_value().filter(
        (value) => getOptionValue(value) !== event.target.name
      ),
    ];
    if (event.target.checked) {
      //if the event checkbox is checked, add it to values list
      new_value.push(
        choices?.find((value) => getOptionValue(value) === event.target.name)
      );
    }
    onChange({ target: { name: id, value: new_value } });
  };

  return (
    <FormControl
      component="fieldset"
      fullWidth
      {...props}
      error={Boolean(errors[id]) && !touched[id]}
    >
      {label && <FormLabel component="legend">{label}</FormLabel>}
      <FormGroup row={!column} sx={{ justifyContent: "flex-start" }}>
        {choices?.map((choice, i) => (
          <FormControlLabel
            label={
              <Fragment>
                {getOptionLabel(choice)}
                {getOptionHelperText(choice) && (
                  <FormHelperText sx={{ m: 0, mb: 1 }}>
                    {getOptionHelperText(choice)}
                  </FormHelperText>
                )}
              </Fragment>
            }
            key={i}
            name={getOptionValue(choice)}
            sx={{ flex: "1 1 auto" }}
            control={
              <Checkbox
                color="primary"
                size="small"
                checked={getOptionSelected(choice, get_group_value())}
                onChange={handleChange}
              />
            }
          />
        ))}
      </FormGroup>
      <FormHelperText>{get_error_text() || helperText}</FormHelperText>
    </FormControl>
  );
}
