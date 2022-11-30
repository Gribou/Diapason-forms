import React from "react";
import { ToggleButton, Typography, Stack } from "@mui/material";

export default function ButtonField({
  id,
  label,
  values,
  errors,
  touched,
  onChange,
  helperText,
  sx = [],
  ...props
}) {
  //button that acts like a checkbox (boolean value)

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  const handleClick = () =>
    onChange({ target: { name: id, value: !values?.[id] } });

  return (
    <Stack
      sx={[{ flexGrow: 1 }, ...(Array.isArray(sx) ? sx : [sx])]}
      {...props}
      alignItems="stretch"
    >
      <ToggleButton
        color="primary"
        value={id}
        selected={values?.[id]}
        fullWidth
        onClick={handleClick}
        size="small"
      >
        {label}
      </ToggleButton>
      {!!(get_error_text() || helperText) && (
        <Typography
          variant="caption"
          color={errors?.[id] && !touched[id] ? "error" : "textSecondary"}
        >
          {get_error_text() || helperText}
        </Typography>
      )}
    </Stack>
  );
}
