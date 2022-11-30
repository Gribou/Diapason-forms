import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogActions,
  Button,
  DialogContent,
  DialogContentText,
} from "@mui/material";

import { useDialog, useForm } from "features/ui";
import formMappings from "features/forms/mappings";

import { FormTextField } from "components/forms/fields";
import useConfirmationDialog from "./ConfirmationDialog";

export default function usePostItDialog(parent_uuid, form_key) {
  const [postit, setPostIt] = useState();
  const { isOpen, open, close } = useDialog();
  const action_mapping = formMappings[form_key];
  const [add_postit, creation_status] = action_mapping.add_postit();
  const [update_postit, update_status] = action_mapping.update_postit();
  const { values, handleUserInput, reset, handleSubmit } = useForm(
    {
      content: postit?.content || "",
    },
    (values) => {
      if (postit?.pk) {
        update_postit({ pk: postit?.pk, content: values.content });
      } else {
        add_postit({ uuid: parent_uuid, content: values.content });
      }
    }
  );

  const onClose = (confirmed) => {
    if (confirmed) {
      handleSubmit();
    }
    setPostIt();
    reset({ content: "" });
    close();
  };

  useEffect(() => {
    reset(postit || {});
  }, [postit]);

  const display = (
    <Dialog
      open={isOpen}
      onClose={() => onClose(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        {postit?.pk ? "Modifier le postIt" : "Ajouter un postIt"}
      </DialogTitle>
      <DialogContent>
        <DialogContentText>
          Indiquez ci-dessous le contenu de votre postIt
        </DialogContentText>
        <FormTextField
          id="content"
          margin="dense"
          label="Contenu"
          multiline
          rows={6}
          onChange={handleUserInput}
          values={values}
          autoFocus
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={() => onClose(false)} color="primary">
          Annuler
        </Button>
        <Button onClick={() => onClose(true)} color="primary">
          Enregistrer
        </Button>
      </DialogActions>
    </Dialog>
  );

  return {
    open,
    display,
    setPostIt,
    isLoading: creation_status?.isLoading || update_status?.isLoading,
  };
}

export function useDestroyConfirmationDialog(parent_uuid, form_key) {
  const [postit, setPostIt] = useState();
  const [destroy_postit, { isLoading }] =
    formMappings[form_key].destroy_postit();

  const { open, display } = useConfirmationDialog({
    title: "Suppression du postIt",
    message: "Etes-vous sûr de vouloir supprimer ce postIt ?",
    onConfirm: () => destroy_postit({ pk: postit?.pk, parent: parent_uuid }),
  });

  return { open, display, setPostIt, isLoading };
}
