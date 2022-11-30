import React, { useEffect } from "react";
import { darken } from "@mui/material/styles";
import { LoadingButton } from "@mui/lab";
import { useSsoLoginMutation } from "features/auth/hooks";

export default function SsoLoginButton({ sx = [], ...props }) {
  const [loginSso, initSsoStatus] = useSsoLoginMutation();
  const { authorization_url } = initSsoStatus?.data || {};

  useEffect(() => {
    // redirect to authorization url (on keycloak server)
    if (initSsoStatus?.isSuccess) {
      window.location.replace(authorization_url);
    }
  }, [initSsoStatus?.isSuccess, authorization_url]);

  return (
    <LoadingButton
      fullWidth
      variant="contained"
      loading={initSsoStatus?.isLoading}
      onClick={() => loginSso()}
      sx={[
        {
          bgcolor: "primary.dark",
          "&:hover": {
            bgcolor: (theme) => darken(theme.palette.primary.dark, 0.2),
          },
        },
        ...(Array.isArray(sx) ? sx : [sx]),
      ]}
      {...props}
    >
      Connexion Angélique
    </LoadingButton>
  );
}
