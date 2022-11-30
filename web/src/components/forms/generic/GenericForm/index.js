import React from "react";
import { Stack } from "@mui/material";
import ErrorBox from "components/misc/ErrorBox";
import GenericFormFooter from "./GenericFormFooter";

export default function GenericForm({
  data = {},
  status = {},
  validatorMode = false,
  investigatorMode = false,
  children,
  onSubmit,
  onCancel,
  formKey,
}) {
  const { isLoading, error } = status;

  return (
    <Stack sx={{ width: "100%", mt: 1 }}>
      <ErrorBox
        errorList={[error?.non_field_errors, error?.detail]}
        sx={{ mb: 2 }}
      />
      {children}
      <GenericFormFooter
        status={data?.status}
        loading={isLoading}
        validatorMode={validatorMode}
        investigatorMode={investigatorMode}
        onSubmit={onSubmit}
        onCancel={onCancel}
        formKey={formKey}
      />
    </Stack>
  );
}
