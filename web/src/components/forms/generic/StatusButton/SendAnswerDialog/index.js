import React, { useEffect } from "react";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  CircularProgress,
  Divider,
} from "@mui/material";
import { Plus } from "mdi-material-ui";
import ErrorBox from "components/misc/ErrorBox";
import { useDialog, useForm, addRow } from "features/ui";
import formMappings from "features/forms/mappings";
import { FormTextField } from "components/forms/fields";
import { cleanEmail } from "features/forms/shared/utils";
import RedactorSubForm from "./RedactorSubForm";
import AttachmentSubForm from "./AttachmentSubForm";

export default function useSendAnswerDialog(uuid, form_key, current_answer) {
  const { isOpen, open, close } = useDialog();
  const [send_answer, { isLoading, isSuccess, error }] =
    formMappings[form_key].send_answer();
  const { values, touched, handleUserInput, reset } = useForm(current_answer);

  useEffect(() => {
    reset(current_answer);
  }, [current_answer]);

  useEffect(() => {
    if (isSuccess) {
      reset(current_answer);
      close();
    }
  }, [isSuccess]);

  const onSubmit = ({ redactors, answer, attachments }) =>
    send_answer({
      uuid,
      answer,
      attachments: attachments?.filter(({ include }) => include),
      redactors: redactors?.map(({ email, ...r }) => ({
        email: cleanEmail(email),
        ...r,
      })),
    });

  const onClose = (confirmed) => {
    if (confirmed) {
      onSubmit(values);
    } else {
      close();
    }
  };

  const form_props = {
    values,
    errors: error,
    touched,
    onChange: handleUserInput,
  };

  const display = (
    <Dialog
      open={isOpen}
      onClose={() => onClose(false)}
      fullWidth
      maxWidth="md"
    >
      <DialogTitle>Envoyer la réponse aux rédacteurs</DialogTitle>
      <DialogContent>
        <ErrorBox errorList={[error?.non_field_errors]} noKeys />
        <DialogContentText
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <span>Renseignez les adresses e-mail des destinataires :</span>
          <Button
            sx={{ ml: "auto" }}
            size="small"
            variant="outlined"
            onClick={() => addRow("redactors", values, handleUserInput)}
            startIcon={<Plus />}
          >
            Destinataire
          </Button>
        </DialogContentText>
        {values?.redactors?.map((r, i) => (
          <RedactorSubForm key={i} {...form_props} index={i} />
        ))}
        <Divider sx={{ my: 2 }} />
        <DialogContentText>
          Sélectionnez les pièces jointes à inclure dans l&apos;email de réponse
          :
        </DialogContentText>
        {values?.attachments?.map((a, i) => (
          <AttachmentSubForm key={i} {...form_props} index={i} />
        ))}
        <FormTextField
          multiline
          required
          rows={6}
          id="answer"
          label="Réponse"
          {...form_props}
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
