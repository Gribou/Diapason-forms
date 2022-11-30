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
import KeywordsSelectField from "components/forms/fields/KeywordsSelectField";
import { useMetaQuery } from "features/config/hooks";

export default function useKeywordsDialog(uuid, form_key, current_value) {
  const { isOpen, open, close } = useDialog();
  const [set_keywords, { isLoading, error, isSuccess }] =
    formMappings[form_key]?.set_keywords() || [];
  const { values, touched, handleUserInput, reset } = useForm({
    keywords: current_value,
  });
  const { data } = useMetaQuery();
  const available_keywords = data?.forms?.[form_key]?.keywords || [];

  useEffect(() => {
    reset({
      keywords: current_value,
    });
  }, [current_value]);

  const onSubmit = (keywords) => set_keywords({ uuid, keywords });

  const onClose = (confirmed) => {
    if (confirmed) {
      onSubmit(values.keywords);
    } else {
      close();
    }
  };

  useEffect(() => {
    if (isSuccess) {
      reset({ keywords: "" });
      close();
    }
  }, [isSuccess]);

  const display = (
    <Dialog open={isOpen} onClose={() => onClose(false)}>
      <DialogTitle>Ajouter des mots clés</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Vous pouvez indiquer ci-dessous des mots-clés permettant de mettre en
          évidence certains types de fiches dans la liste à traiter.
        </DialogContentText>
        <DialogContentText>
          Laissez vide pour n&apos;indiquer aucun mot-clé.
        </DialogContentText>
        <ErrorBox errorDict={error} noKeys />
        <KeywordsSelectField
          id="keywords"
          label="Mots-clés"
          placeholder="Ex: 4F FIR FRA"
          helperText="Appuyer sur ENTREE entre chaque mot-clé"
          onChange={handleUserInput}
          choices={available_keywords}
          inputProps={{ maxLength: 250 }}
          values={values}
          errors={error}
          touched={touched}
          autoFocus
          sx={{ mt: 2 }}
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
