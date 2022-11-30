import React, { Fragment } from "react";
import { Grid, Button } from "@mui/material";

export default function InvestigatorFormFooter({
  loading,
  handleSubmit,
  onCancel,
}) {
  return (
    <Fragment>
      <Grid xs item>
        <Button
          fullWidth
          variant="outlined"
          color="primary"
          disabled={loading}
          onClick={onCancel}
        >
          Annuler
        </Button>
      </Grid>
      <Grid xs item>
        <Button
          fullWidth
          variant="contained"
          color="primary"
          disabled={loading}
          onClick={(e) => handleSubmit(e, { proceed: false })}
        >
          Enregistrer les modifications
        </Button>
      </Grid>
    </Fragment>
  );
}
