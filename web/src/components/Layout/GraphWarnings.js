import React from "react";
import { Stack, Alert } from "@mui/material";
import { useGraphCompleteness } from "features/config/hooks";

function GraphWarning({ label, checked, complete }) {
  return !checked ? (
    <Alert severity="warning">
      {`
      La configuration des ${label} n'a pas été vérifiée (graphes
      d'actions). Veuillez contacter l'administrateur.`}
    </Alert>
  ) : (
    !complete && (
      <Alert severity="error">
        {`Les ${label} sont malconfigurées (graphes d'actions). Veuillez contacter l'administrateur.`}
      </Alert>
    )
  );
}

export default function GraphWarnings() {
  const { fne, simi, brouillage, isSuccess } = useGraphCompleteness();

  return (
    isSuccess && (
      <Stack>
        <GraphWarning {...fne?.graph} label="FNE" />
        <GraphWarning {...simi?.graph} label="Fiches Similitude d'Indicatifs" />
        <GraphWarning {...brouillage?.graph} label="Fiches Brouillage" />
      </Stack>
    )
  );
}
