import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";

import { useDialog, useForm } from "features/ui";
import { useMetaQuery, useFormConfig } from "features/config/hooks";
import { SIMI_FORM_KEY } from "features/forms/mappings";
import { FormTextField, KeywordsSelectField } from "components/forms/fields";

export default function useSubDataDialog(data, onSubmit) {
  const { isOpen, open, close } = useDialog();
  const { safetycube_enabled } = useFormConfig(SIMI_FORM_KEY);
  const { values, handleUserInput, handleSubmit } = useForm(data, onSubmit);
  const { data: meta } = useMetaQuery();
  const available_keywords = meta?.forms?.[SIMI_FORM_KEY]?.keywords || [];

  const onClose = (confirmed) => {
    if (confirmed) {
      handleSubmit();
    }
    close();
  };

  const form_props = {
    values: { keywords: values?.keywords, ...values?.sub_data },
    onChange: (event) => {
      if (event.target.name === "keywords") handleUserInput(event);
      else {
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
      <DialogTitle>Enquête Similitude d&apos;Indicatifs</DialogTitle>
      <DialogContent>
        {!safetycube_enabled && (
          <FormTextField
            id="inca_number"
            label="Numéro INCA"
            helperText="(ex : EX21LFFF1234)"
            {...form_props}
          />
        )}
        <KeywordsSelectField
          id="keywords"
          label="Mots-clés"
          placeholder="Ex: 4F FIR FRA"
          choices={available_keywords}
          inputProps={{ maxLength: 250 }}
          helperText="Appuyer sur ENTREE entre chaque différent mot-clé"
          {...form_props}
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
