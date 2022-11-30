import React from "react";
import { Grid, Button } from "@mui/material";

export default function ValidatorFormFooter({
  loading,
  handleSubmit,
  proceed,
}) {
  return (
    <Grid xs item>
      <Button
        fullWidth
        variant="contained"
        color="primary"
        disabled={loading}
        onClick={(e) => handleSubmit(e, { proceed })}
      >
        Valider
      </Button>
    </Grid>
  );
}
