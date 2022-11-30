import React, { Fragment } from "react";
import { Grid, Button } from "@mui/material";
import { useAuthenticated } from "features/auth/hooks";
import { useFormConfig } from "features/config/hooks";

export default function DraftFormFooter({
  loading,
  handleSubmit,
  me,
  formKey,
}) {
  const is_authenticated = useAuthenticated();
  const { save_button_label } = useFormConfig(formKey);
  return (
    <Fragment>
      {!is_authenticated && (
        <Grid xs item>
          <Button
            fullWidth
            variant="outlined"
            color="primary"
            disabled={loading}
            onClick={(e) => handleSubmit(e, { proceed: false })}
          >
            Enregistrer le brouillon
          </Button>
        </Grid>
      )}
      <Grid xs item>
        <Button
          fullWidth
          variant="contained"
          color="primary"
          disabled={loading}
          onClick={(e) =>
            handleSubmit(e, {
              proceed: true,
              bypass_validation: me?.is_validator || me?.has_all_access,
            })
          }
        >
          {me?.has_all_access
            ? "Enregistrer"
            : me?.is_validator
            ? "Valider"
            : save_button_label || "Envoyer au CDS"}
        </Button>
      </Grid>
    </Fragment>
  );
}
