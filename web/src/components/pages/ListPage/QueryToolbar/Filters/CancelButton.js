import React from "react";
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material";
import { Cancel } from "mdi-material-ui";
import { useSearchParams } from "features/router";

export default function CancelButton({ onClose }) {
  const [{ form_key, search }, push] = useSearchParams();

  const onClick = () => {
    push({ form_key, search });
    onClose();
  };

  return (
    <MenuItem dense onClick={onClick}>
      <ListItemIcon>
        <Cancel />
      </ListItemIcon>
      <ListItemText>Tout afficher</ListItemText>
    </MenuItem>
  );
}
