import React from "react";
import moment from "moment-timezone";
import { DatePicker } from "@mui/x-date-pickers";
import { Calendar } from "mdi-material-ui";
import { TextField, useMediaQuery, InputAdornment } from "@mui/material";
import { DATE_DATA_FORMAT } from "constants/config";

export default function FormDateField({
  id,
  label,
  values,
  errors,
  touched,
  onChange,
  required,
  ...props
}) {
  const desktopMode = useMediaQuery("(pointer: fine)");

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <DatePicker
      id={id}
      name={id}
      value={values?.[id] || null}
      toolbarTitle="Sélectionner date"
      toolbarFormat="DD MMM"
      onChange={(value) =>
        onChange({
          target: {
            name: id,
            value: value && moment(value).format(DATE_DATA_FORMAT),
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
          required={required}
          error={Boolean(errors[id]) && !touched[id]}
          helperText={get_error_text() || ""}
          InputProps={{
            ...InputProps,
            ...(desktopMode
              ? {}
              : {
                  endAdornment: (
                    <InputAdornment position="end">
                      <Calendar />
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
