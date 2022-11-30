import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import { useLogoutMutation } from "features/auth/hooks";
import { ROUTES } from "routes";

export default function LogoutButton() {
  const navigate = useNavigate();
  const [logout, { isSuccess }] = useLogoutMutation();

  useEffect(() => {
    if (isSuccess) {
      navigate(ROUTES.home.path);
    }
  }, [isSuccess]);

  return (
    <Button
      variant="outlined"
      size="small"
      color="inherit"
      onClick={() => logout()}
      edge="end"
    >
      Déconnexion
    </Button>
  );
}
