import React from "react";
import { Grid } from "@mui/material";

import { useMe } from "features/auth/hooks";
import DraftFormFooter from "./DraftFormFooter";
import InvestigatorFormFooter from "./InvestigatorFormFooter";
import ValidatorFormFooter from "./ValidatorFormFooter";

export default function GenericFormFooter({
  loading,
  status,
  validatorMode = false,
  investigatorMode = false,
  onSubmit,
  onCancel,
  formKey,
}) {
  const me = useMe();
  const draftMode = !validatorMode && !investigatorMode;
  return (
    <Grid container spacing={1} sx={{ my: 1 }}>
      {draftMode && (
        <DraftFormFooter
          me={me}
          loading={loading}
          handleSubmit={onSubmit}
          formKey={formKey}
        />
      )}
      {validatorMode && (
        <ValidatorFormFooter
          loading={loading}
          proceed={!status?.is_done}
          handleSubmit={onSubmit}
        />
        //Do not auto apply next action if the form is marked as 'done'
        //This is used when a validator edits a form which is already validated. We don't want the form to be sent to investigators right away
      )}
      {investigatorMode && (
        <InvestigatorFormFooter
          loading={loading}
          handleSubmit={onSubmit}
          onCancel={onCancel}
        />
      )}
    </Grid>
  );
}
