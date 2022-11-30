import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Alert,
} from "@mui/material";
import { useDialog } from "features/ui";

export default function useWarnCdsDialog(onClose = () => {}) {
  const { isOpen, open, close } = useDialog();

  const handleClose = () => {
    close();
    onClose();
  };

  const display = (
    <Dialog open={isOpen} onClose={close} maxWidth="md">
      <DialogTitle>Fiche envoyée</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Votre fiche a bien été enregistrée et envoyée au CDS.
        </DialogContentText>
        <DialogContentText component={Alert} severity="warning">
          Prévenez-le oralement pour qu&apos;il puisse la traiter !
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>OK</Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
