import React from "react";
import { TextField, Checkbox, Autocomplete } from "@mui/material";

export default function KeywordSelectField({
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

  const handleChange = (e, value) => {
    onChange({ target: { name: id, value } });
  };

  return (
    <Autocomplete
      multiple
      id={id}
      name={id}
      options={choices || []}
      freeSolo
      autoSelect
      clearOnBlur
      fullWidth
      value={
        Array.isArray(values?.[id])
          ? values?.[id]
          : values?.[id]?.trim()?.split(" ") || []
      }
      onChange={handleChange}
      renderOption={(props, option, { selected }) => (
        <li {...props}>
          <Checkbox sx={{ mr: 2 }} checked={selected} />
          {option}
        </li>
      )}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          required={required}
          margin="dense"
          size="small"
          error={Boolean(errors[id]) && !touched[id]}
          helperText={get_error_text() || helperText}
          {...inputProps}
        />
      )}
      {...props}
    />
  );
}
