import React from "react";
import {
  ToggleButtonGroup,
  ToggleButton,
  Typography,
  Stack,
} from "@mui/material";

export default function ButtonField({
  id,
  label,
  values,
  errors,
  touched,
  onChange,
  helperText,
  choices,
  required,
  sx = [],
  ...props
}) {
  //button group that acts like a select (single value)

  const get_error_text = () => {
    const error = errors?.[id];
    if (Array.isArray(error)) return error.join(" ");
    else return error;
  };

  const handleClick = (e, value) => {
    if (!required || value !== null) onChange({ target: { name: id, value } });
  };

  return (
    <Stack
      direction="row"
      sx={[{ flexGrow: 1 }, ...(Array.isArray(sx) ? sx : [sx])]}
      {...props}
      alignItems="center"
    >
      <Stack sx={{ mr: 1 }}>
        <Typography
          variant="overline"
          noWrap
          sx={{ mr: 1, lineHeight: 1 }}
          color={errors?.[id] && !touched[id] ? "error" : "textPrimary"}
        >
          {`${label}${required ? " *" : ""} : `}
        </Typography>
        {!!(get_error_text() || helperText) && (
          <Typography
            variant="caption"
            color={errors?.[id] && !touched[id] ? "error" : "textSecondary"}
          >
            {get_error_text() || helperText}
          </Typography>
        )}
      </Stack>
      <ToggleButtonGroup
        color="primary"
        value={values?.[id]}
        exclusive
        onChange={handleClick}
        fullWidth
        size="small"
        sx={{ flexGrow: 1, width: "unset" }}
      >
        {choices?.map((c) => (
          <ToggleButton key={c} value={c}>
            {c}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Stack>
  );
}
