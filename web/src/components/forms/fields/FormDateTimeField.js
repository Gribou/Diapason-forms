import React, { Fragment } from "react";
import moment from "moment-timezone";
import { DateTimePicker } from "@mui/x-date-pickers";
import { Alert, TextField, InputAdornment, useMediaQuery } from "@mui/material";
import { Calendar } from "mdi-material-ui";
import { DATETIME_DATA_FORMAT } from "constants/config";

export default function FormDateTimeField({
  id,
  label,
  values,
  errors,
  touched,
  onChange,
  required,
  helperText = "",
  warnIfOlderThanHours,
  ...props
}) {
  const desktopMode = useMediaQuery("(pointer: fine)");

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <Fragment>
      <DateTimePicker
        id={id}
        name={id}
        value={values?.[id] || null}
        toolbarTitle="Sélectionner date et heure"
        toolbarFormat="DD MMM"
        onChange={(value) =>
          onChange({
            target: {
              name: id,
              value: value && moment(value).format(DATETIME_DATA_FORMAT),
            },
          })
        }
        renderInput={({ InputProps, ...params }) => (
          <TextField
            {...params}
            label={label}
            margin="dense"
            required={required}
            size="small"
            fullWidth
            error={Boolean(errors[id]) && !touched[id]}
            helperText={get_error_text() || helperText}
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
      {warnIfOlderThanHours &&
        moment
          .tz(values[id], "UTC")
          .isBefore(moment().subtract(warnIfOlderThanHours, "hours")) && (
          <Alert severity="warning" align="justify">
            {`Cette valeur a plus de ${warnIfOlderThanHours} heures.`}
          </Alert>
        )}
    </Fragment>
  );
}
