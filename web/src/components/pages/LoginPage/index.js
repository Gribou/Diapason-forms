import React from "react";
import { Navigate } from "react-router-dom";
import { Box } from "@mui/material";
import { useAuthenticated, useSsoLoginCallback } from "features/auth/hooks";
import { ROUTES } from "routes";

import useLoginForm from "./LoginForm";
import ErrorBox from "components/misc/ErrorBox";
import AuthPage from "./AuthPage";

export default function LoginPage() {
  const is_authenticated = useAuthenticated();
  const form = useLoginForm();
  const sso = useSsoLoginCallback();

  const errorbox = (
    <Box sx={{ mt: 2, width: "100%" }}>
      <ErrorBox
        errorList={[
          form?.errors?.non_field_errors,
          sso?.error?.non_field_errors,
        ]}
      />
    </Box>
  );

  return is_authenticated ? (
    <Navigate to={ROUTES.home.path} />
  ) : (
    <AuthPage loading={form.loading} title="Connexion">
      {errorbox}
      {form.display}
    </AuthPage>
  );
}
