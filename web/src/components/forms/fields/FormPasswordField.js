import React, { useState } from "react";
import { InputAdornment, IconButton } from "@mui/material";
import FormTextField from "./FormTextField";
import { Eye, EyeOff } from "mdi-material-ui";

export default function PasswordTextField(props) {
  const [showPassword, setShowPassword] = useState(false);

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <FormTextField
      {...props}
      fullWidth
      type={showPassword ? "text" : "password"}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <IconButton
              aria-label="toggle password visibility"
              onClick={handleClickShowPassword}
              onMouseDown={handleMouseDownPassword}
              edge="end"
            >
              {showPassword ? <EyeOff /> : <Eye />}
            </IconButton>
          </InputAdornment>
        ),
      }}
    />
  );
}
