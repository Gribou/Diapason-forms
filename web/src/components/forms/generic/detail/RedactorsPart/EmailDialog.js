import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  InputAdornment,
  DialogActions,
  Button,
} from "@mui/material";
import { useDialog } from "features/ui";
import FormTextField from "components/forms/fields/FormTextField";

export default function useEmailDialog(formProps) {
  const { isOpen, open, close } = useDialog();
  const { onChange } = formProps;

  const handleClear = () => onChange({ target: { name: "email", value: "" } });

  const display = (
    <Dialog open={isOpen} onClose={close}>
      <DialogTitle>Notifications d&apos;avancement</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Renseignez votre adresse e-mail professionnelle ci-dessous si vous
          souhaitez être informé automatiquement de l&apos;avancement du
          traitement de votre fiche.
        </DialogContentText>
        <FormTextField
          id="email"
          InputProps={{
            placeholder: "prenom.nom",
            endAdornment: (
              <InputAdornment position="end">
                @aviation-civile.gouv.fr
              </InputAdornment>
            ),
          }}
          {...formProps}
        />
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={handleClear}>
          Effacer
        </Button>
        <Button color="primary" onClick={close}>
          Fermer
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
