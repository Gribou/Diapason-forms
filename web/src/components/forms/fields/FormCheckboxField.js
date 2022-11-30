import React, { Fragment } from "react";
import {
  FormControlLabel,
  Checkbox,
  FormControl,
  FormHelperText,
} from "@mui/material";

export default function FormCheckboxField({
  id,
  values,
  errors = {},
  touched,
  label,
  onChange,
  helperText,
  ...props
}) {
  const get_error_text = () => {
    const error = errors[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <FormControl
      fullWidth
      {...props}
      error={Boolean(errors[id]) && !touched[id]}
    >
      <FormControlLabel
        label={
          <Fragment>
            {label}
            <FormHelperText sx={{ ml: 0, mt: 0 }}>
              {get_error_text() || helperText}
            </FormHelperText>
          </Fragment>
        }
        id={id}
        name={id}
        control={
          <Checkbox
            color="primary"
            size="small"
            checked={(values && values[id]) || false}
            onChange={(e) =>
              onChange({
                target: {
                  name: e.target.name,
                  value: e.target.checked,
                },
              })
            }
          />
        }
      />
    </FormControl>
  );
}
