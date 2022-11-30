import React, { useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";

import { useDialog, useForm } from "features/ui";
import { useMetaQuery, useFormConfig } from "features/config/hooks";
import { HN_CHOICES } from "constants/fne";
import { FNE_FORM_KEY } from "features/forms/mappings";
import {
  FormTextField,
  FormSelectField,
  FormCheckboxField,
  KeywordsSelectField,
} from "components/forms/fields";

export default function useSubDataDialog(fne, onSubmit) {
  const { isOpen, open, close } = useDialog();
  const { safetycube_enabled } = useFormConfig(FNE_FORM_KEY);
  const { values, handleUserInput, handleSubmit, reset } = useForm(
    fne,
    onSubmit
  );
  const { data: meta } = useMetaQuery();
  const available_keywords = meta?.forms?.[FNE_FORM_KEY]?.keywords || [];

  useEffect(() => {
    reset(fne);
  }, [fne]);

  const onClose = (confirmed) => {
    if (confirmed) {
      handleSubmit();
    }
    close();
  };

  const form_props = {
    values: { keywords: values?.keywords, ...values?.sub_data },
    onChange: (event) => {
      if (event.target.name === "keywords") {
        handleUserInput(event);
      } else {
        handleUserInput({
          target: {
            name: "sub_data",
            value: {
              ...values?.sub_data,
              [event.target.name]: event.target.value,
            },
          },
        });
      }
    },
  };

  const display = (
    <Dialog
      open={isOpen}
      onClose={() => onClose(false)}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle>Enquête FNE</DialogTitle>
      <DialogContent>
        {!safetycube_enabled && (
          <FormTextField
            id="inca_number"
            label="Numéro INCA"
            helperText="(ex : EX21LFFF1234)"
            {...form_props}
          />
        )}
        <FormSelectField
          id="hn"
          label="HN/ASR"
          choices={HN_CHOICES}
          getOptionLabel={(option) => (option ? `${option}` : "Non")}
          {...form_props}
        />
        <FormCheckboxField
          id="is_safety_event"
          label="Evènement Sécurité"
          helperText="Devra être traité dans les 90 jours."
          {...form_props}
          sx={{ mt: 2 }}
        />
        <KeywordsSelectField
          id="keywords"
          label="Mots-clés"
          placeholder="Ex: 4F FIR FRA"
          choices={available_keywords}
          inputProps={{ maxLength: 250 }}
          helperText="Appuyer sur ENTREE entre chaque différent mot-clé"
          {...form_props}
          sx={{ mt: 2 }}
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

  return { open, display };
}
