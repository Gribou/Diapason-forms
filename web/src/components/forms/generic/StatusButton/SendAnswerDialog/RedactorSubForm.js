import React from "react";

import { Typography, Stack, InputAdornment, IconButton } from "@mui/material";
import { Delete } from "mdi-material-ui";
import { useSubForm } from "features/ui";
import { FormSelectField } from "components/forms/fields";

export default function RedactorSubForm({
  values,
  error,
  touched,
  onChange,
  index,
}) {
  const { handleChange, handleDelete } = useSubForm({
    index,
    root_key: "redactors",
    values,
    onChange,
  });

  const form_props = {
    values: values?.redactors?.[index],
    errors: error?.redactors?.[index],
    touched: touched?.redactors?.[index],
  };

  const item = values?.redactors?.[index];

  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="stretch"
      spacing={2}
      sx={{ py: 1 }}
    >
      <Typography sx={{ minWidth: "30%" }}>
        {item?.display_name || "Destinataire additionnel"}
      </Typography>
      <FormSelectField
        id="email"
        margin="dense"
        label="Adresse e-mail"
        freeSolo
        choices={item?.suggestions}
        {...form_props}
        onChange={(event) => handleChange(event, "email")}
        inputProps={{
          InputProps: {
            placeholder: "prenom.nom",
            endAdornment: (
              <InputAdornment position="end">
                @aviation-civile.gouv.fr
              </InputAdornment>
            ),
          },
        }}
      />
      <IconButton
        disabled={!!item?.display_name}
        color="error"
        onClick={handleDelete}
        sx={{ mt: 1 }}
      >
        <Delete />
      </IconButton>
    </Stack>
  );
}
