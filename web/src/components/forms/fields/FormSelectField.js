import React from "react";
import { TextField, Autocomplete } from "@mui/material";

export default function FormSelectField({
  id,
  values,
  errors = {},
  touched = {},
  helperText,
  label,
  onChange,
  choices,
  inputProps,
  required,
  ...props
}) {
  const get_error_text = () => {
    const error = errors[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <Autocomplete
      id={id}
      name={id}
      options={choices || []}
      getOptionLabel={(choice) => `${choice}`}
      isOptionEqualToValue={(option, value) => value === "" || option === value}
      fullWidth
      autoComplete
      autoSelect
      autoHighlight
      value={(values && values[id]) || ""}
      onChange={(e, value) => onChange({ target: { name: id, value } })}
      renderInput={({ InputProps, ...params }) => (
        <TextField
          {...params}
          label={label}
          margin="dense"
          size="small"
          required={required}
          error={Boolean(errors[id]) && !touched[id]}
          helperText={get_error_text() || helperText}
          {...inputProps}
          InputProps={{
            ...InputProps,
            ...(inputProps?.InputProps || {}),
          }}
        />
      )}
      {...props}
    />
  );
}
