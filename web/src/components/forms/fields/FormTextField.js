import React from "react";
import { TextField } from "@mui/material";

export default function FormTextField({
  id,
  values,
  errors = {},
  touched = {},
  onChange,
  pattern,
  helperText = "",
  ...props
}) {
  const get_error_text = () => {
    const error = errors[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  const handleChange = ({ target }) => {
    if (!pattern || pattern.test(target.value)) {
      onChange({ target: { name: target.name, value: target.value } });
    }
  };

  return (
    <TextField
      margin="dense"
      size="small"
      fullWidth
      autoComplete="off"
      id={id}
      name={id}
      value={(values && values[id]) || ""}
      error={Boolean(errors[id]) && !touched[id]}
      helperText={get_error_text() || helperText}
      FormHelperTextProps={{ margin: "dense" }}
      {...props}
      onChange={handleChange}
    />
  );
}
