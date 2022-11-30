import React, { useEffect, Fragment } from "react";
import { Button, Stack, Divider } from "@mui/material";
import FormTextField from "components/forms/fields/FormTextField";
import PasswordTextField from "components/forms/fields/FormPasswordField";
import { useFeatures } from "features/config/hooks";
import { useLoginMutation } from "features/auth/hooks";
import { useForm } from "features/ui";
import SsoLoginButton from "./SsoLoginButton";

export default function useLoginForm() {
  const { sso } = useFeatures();
  const [login, { isLoading, error, isSuccess, reset }] = useLoginMutation();
  const { values, touched, handleUserInput, handleSubmit } = useForm(
    { username: "", password: "" },
    login
  );

  useEffect(() => {
    reset();
  }, []); //reset mutation state when component loads

  const form_props = {
    values,
    touched,
    errors: error,
    onChange: handleUserInput,
  };

  const display = (
    <Stack
      component="form"
      sx={{ width: "100%", mt: 1 }}
      noValidate
      onSubmit={handleSubmit}
    >
      <FormTextField
        margin="normal"
        size="medium"
        required
        fullWidth
        id="username"
        label="Nom d'utilisateur"
        autoComplete="username"
        autoFocus
        {...form_props}
      />
      <PasswordTextField
        margin="normal"
        size="medium"
        required
        fullWidth
        id="password"
        label="Mot de passe"
        autoComplete="current-password"
        {...form_props}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2, mb: 2 }}
      >
        Connexion
      </Button>
      {sso && (
        <Fragment>
          <Divider flexItem sx={{ mb: 2 }} />
          <SsoLoginButton />
        </Fragment>
      )}
    </Stack>
  );

  return {
    loading: isLoading,
    errors: error || {},
    success: isSuccess,
    display,
  };
}
