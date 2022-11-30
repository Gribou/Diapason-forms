import React from "react";
import {
  DialogTitle,
  Dialog,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@mui/material";
import { useDialog } from "features/ui";

export default function useConfirmationDialog({
  title,
  message,
  messages,
  onConfirm,
  onCancel,
}) {
  const { isOpen, open, close } = useDialog();

  if (message) {
    messages = [message];
  }

  const onClose = (confirmed) => {
    if (confirmed) {
      onConfirm();
    } else if (onCancel) {
      onCancel();
    }
    close();
  };

  const display = (
    <Dialog
      open={isOpen}
      onClose={() => onClose(false)}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
      {messages && (
        <DialogContent>
          {messages.map((m, i) => (
            <DialogContentText key={i} align="justify">
              {m}
            </DialogContentText>
          ))}
        </DialogContent>
      )}
      <DialogActions>
        <Button onClick={() => onClose(false)} color="primary">
          Annuler
        </Button>
        <Button onClick={() => onClose(true)} color="primary" autoFocus>
          Ok
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { open, display };
}
