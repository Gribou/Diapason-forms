import React from "react";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from "@mui/material";

import FormCheckboxGroupField from "components/forms/fields/FormCheckboxGroupField";
import useGenericPreSubmitCheckDialog from "components/forms/generic/dialogs/GenericPreSubmitCheckDialog";
import { makeTechActionsToDo, techActionsComplete } from "../utils";

export default function useTechActionsDialog(formProps) {
  const { isOpen, open, close, handleConfirm } = useGenericPreSubmitCheckDialog(
    formProps,
    "force_tech_actions"
  );
  const tech_actions_to_do = makeTechActionsToDo(formProps?.values);

  const is_complete = () =>
    techActionsComplete(
      formProps?.values?.tech_actions_done || [],
      tech_actions_to_do
    );

  const display = (
    <Dialog open={isOpen} onClose={close}>
      <DialogTitle>Actions à entreprendre</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Vous allez signaler un évènement technique. Certaines actions doivent
          être effectuées afin de faciliter son traitement par les subdivisions.
          <br />
          Avez-vous effectué les actions suivantes ?
        </DialogContentText>
        <FormCheckboxGroupField
          id="tech_actions_done"
          choices={tech_actions_to_do}
          getOptionLabel={(choice) => choice?.name}
          getOptionHelperText={(choice) => choice?.helperText}
          {...formProps}
        />
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={close}>
          Annuler
        </Button>
        <Button color="primary" onClick={handleConfirm}>
          {`Envoyer${is_complete() ? "" : " quand même"}`}
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
