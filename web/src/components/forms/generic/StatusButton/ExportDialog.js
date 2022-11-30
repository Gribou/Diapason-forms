import React from "react";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@mui/material";
import { useDialog } from "features/ui";
import formMappings from "features/forms/mappings";

export default function useExportDialog(uuid, form_key) {
  const { isOpen, open, close } = useDialog();
  const [export_form, { isLoading }] = formMappings[form_key].export();

  const onClose = (confirmed, anonymous) => {
    if (confirmed) {
      onConfirmed(anonymous);
    }
    close();
  };

  const onConfirmed = (anonymous) => export_form({ uuid, anonymous });

  const display = (
    <Dialog open={isOpen} onClose={() => onClose(false)}>
      <DialogTitle>Export au format PDF</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Le contenu du fichier exporté doit-il être anonymisé ?
        </DialogContentText>
        <DialogContentText>
          Les rédacteurs de la fiche ne seront pas inclus dans le fichier
          exporté.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => onClose(false)} color="primary">
          Annuler
        </Button>
        <Button
          onClick={() => onClose(true, true)}
          color="primary"
          autoFocus
          style={{ marginLeft: "auto" }}
        >
          Oui
        </Button>
        <Button onClick={() => onClose(true, false)} color="primary">
          Non
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, isLoading, open };
}
