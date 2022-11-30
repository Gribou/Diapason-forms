import React from "react";
import {
  FormLabel,
  FormControl,
  RadioGroup,
  FormControlLabel,
  FormHelperText,
  Radio,
} from "@mui/material";

export default function FormRadioField({
  id,
  values,
  errors,
  touched,
  label,
  onChange,
  choices,
  helperText,
  boolean,
  radioSx,
  legendComponent = "legend",
  legendSx = {},
  ...props
}) {
  const handleChange = (e) =>
    onChange(
      boolean
        ? {
            target: {
              name: e.target.name,
              value: e.target.value === "true",
            },
          }
        : e
    );

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  return (
    <FormControl
      component="fieldset"
      fullWidth
      {...props}
      error={Boolean(errors?.[id]) && !touched?.[id]}
    >
      {label && (
        <FormLabel component={legendComponent} sx={legendSx}>
          {label}
        </FormLabel>
      )}
      <RadioGroup
        row
        sx={{ justifyContent: "space-between" }}
        name={id}
        id={id}
        value={boolean ? !!values?.[id] : values?.[id] || ""}
        onChange={handleChange}
      >
        {choices.map((choice, i) => (
          <FormControlLabel
            {...choice}
            sx={radioSx}
            key={i}
            control={<Radio size="small" />}
          />
        ))}
      </RadioGroup>
      {(helperText || Boolean(errors?.[id])) && (
        <FormHelperText>{get_error_text() || helperText}</FormHelperText>
      )}
    </FormControl>
  );
}
