import React from "react";
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material";

const handleMutationClick = (payload, trigger, onClose) => {
  trigger(payload);
  onClose();
};

const openDialogOnClick = (dialog, onClose) => {
  dialog.open();
  onClose();
};

export function ActionMenuItem({
  dialog,
  mutation,
  payload,
  icon,
  label,
  onClose,
}) {
  return (
    <MenuItem
      onClick={() =>
        dialog
          ? openDialogOnClick(dialog, onClose)
          : handleMutationClick(payload, mutation?.[0], onClose)
      }
    >
      <ListItemIcon>{icon}</ListItemIcon>
      <ListItemText>{label}</ListItemText>
    </MenuItem>
  );
}
