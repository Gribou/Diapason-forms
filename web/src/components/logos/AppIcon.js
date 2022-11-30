import React from "react";
import { Avatar, CircularProgress } from "@mui/material";
import EFNEIcon from "./EFNEIcon";

export default function AppIcon({ loading, size }) {
  return (
    <Avatar
      sx={{
        m: 1,
        bgcolor: "primary.dark",
        textAlign: "center",
        ...(size === "large"
          ? {
              width: (theme) => theme.spacing(7),
              height: (theme) => theme.spacing(7),
            }
          : {}),
      }}
    >
      {loading ? (
        <CircularProgress sx={{ p: 1, color: "primary.main" }} />
      ) : (
        <EFNEIcon
          sx={{ width: "100%", height: "100%", p: 1 }}
          baseColor="#fff"
          accentColor="#fff"
        />
      )}
    </Avatar>
  );
}
