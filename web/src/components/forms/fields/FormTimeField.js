import React from "react";
import moment from "moment";
import { TimePicker } from "@mui/x-date-pickers";
import { TextField, InputAdornment, useMediaQuery } from "@mui/material";
import { ClockOutline } from "mdi-material-ui";
import { TIME_FORMAT } from "constants/config";

export default function FormTimeField({
  id,
  label,
  values,
  errors,
  touched,
  onChange,
  ...props
}) {
  const desktopMode = useMediaQuery("(pointer: fine)");

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <TimePicker
      id={id}
      name={id}
      value={values?.[id] || null}
      toolbarTitle="Sélectionner heure"
      onChange={(value) =>
        onChange({
          target: {
            name: id,
            value: value && moment(value).format(TIME_FORMAT),
          },
        })
      }
      renderInput={({ InputProps, ...params }) => (
        <TextField
          {...params}
          label={label}
          margin="dense"
          size="small"
          fullWidth
          error={Boolean(errors?.[id]) && !touched?.[id]}
          helperText={get_error_text()}
          InputProps={{
            ...InputProps,
            ...(desktopMode
              ? {}
              : {
                  endAdornment: (
                    <InputAdornment position="end">
                      <ClockOutline />
                    </InputAdornment>
                  ),
                }),
          }}
        />
      )}
      {...props}
    />
  );
}
