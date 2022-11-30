import React, { useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  CircularProgress,
} from "@mui/material";

import { useDialog, useForm } from "features/ui";
import formMappings from "features/forms/mappings";

import ErrorBox from "components/misc/ErrorBox";
import FormTextField from "components/forms/fields/FormTextField";

export default function useAssignPersonDialog(uuid, form_key) {
  const { isOpen, open, close } = useDialog();
  const [assign_to_person, { isLoading, error, isSuccess }] =
    formMappings[form_key]?.assign_to_person() || [];
  const { values, touched, handleUserInput, reset } = useForm({
    next_person: "",
  });

  const onSubmit = (next_person) => assign_to_person({ uuid, next_person });

  const onClose = (confirmed) => {
    if (confirmed) {
      onSubmit(values.next_person);
    } else {
      close();
    }
  };

  useEffect(() => {
    if (isSuccess) {
      reset({ next_person: "" });
      close();
    }
  }, [isSuccess]);

  const display = (
    <Dialog open={isOpen} onClose={() => onClose(false)}>
      <DialogTitle>Attribuer la fiche à une personne</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Indiquez ci-dessous le nom ou le trigramme de la personne traitant la
          fiche.
        </DialogContentText>
        <DialogContentText>
          Laissez vide pour ne l&apos;attribuer à personne en particulier.
        </DialogContentText>
        <ErrorBox errorDict={error} noKeys />
        <FormTextField
          id="next_person"
          margin="dense"
          label="Responsable (nom ou trigramme)"
          onChange={handleUserInput}
          inputProps={{ maxLength: 25 }}
          values={values}
          errors={error}
          touched={touched}
          autoFocus
        />
      </DialogContent>
      <DialogActions>
        {isLoading && <CircularProgress size={24} />}
        <Button
          onClick={() => onClose(false)}
          color="primary"
          disabled={isLoading}
        >
          Annuler
        </Button>
        <Button
          onClick={() => onClose(true)}
          color="primary"
          disabled={isLoading}
        >
          Confirmer
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { open, display, isLoading };
}
