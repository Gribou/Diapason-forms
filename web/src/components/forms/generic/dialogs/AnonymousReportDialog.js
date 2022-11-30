import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@mui/material";

import useGenericPreSubmitCheckDialog from "./GenericPreSubmitCheckDialog";

export const is_anonymous_report = (values) =>
  !values?.redactors?.filter(({ fullname }) => fullname)?.length;

export default function useAnonymousReportDialog(formProps) {
  const { isOpen, open, close, handleConfirm } = useGenericPreSubmitCheckDialog(
    formProps,
    "force_anonymous"
  );

  const display = (
    <Dialog open={isOpen} onClose={close}>
      <DialogTitle>Report d&apos;évènement anonyme</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Vous n&apos;avez pas renseigner le nom du ou des rédacteurs.
          Souhaitez-vous reporter un évènement anonymement ?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={close}>
          Annuler
        </Button>
        <Button color="primary" onClick={handleConfirm}>
          Envoyer anonymement
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
