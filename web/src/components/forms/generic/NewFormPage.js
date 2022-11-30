import React from "react";
import { useNavigate } from "react-router-dom";
import { Container, Typography, CircularProgress, Stack } from "@mui/material";

import ErrorBox from "components/misc/ErrorBox";
import { useMe } from "features/auth/hooks";
import formMappings from "features/forms/mappings";
import { scrollToTop } from "features/ui";
import { useFormConfig } from "features/config/hooks";
import GenericSaveSuccessDialog from "./GenericSaveSuccessDialog";

export default function NewFormPage({
  title,
  formKey,
  defaultData,
  FormComponent,
  showRoute,
  children,
}) {
  const navigate = useNavigate();
  const { has_all_access } = useMe();
  const { enabled } = useFormConfig(formKey);
  const [create, request] = formMappings[formKey].create();
  const { data, ...status } = request;
  const { isError, error, isLoading } = status;

  const redirectAction = () =>
    data?.uuid && navigate(showRoute.path.replace(":pk", data?.uuid));

  //show dialogs depending on options then apply submit function
  //proceed : should default next action be applied
  //bypass_validation : should form be auto validated (cf actions/forms.js)
  const handleSubmit = (values, options) => {
    create({ ...values, options });
    scrollToTop();
  };

  const get_error_message = () =>
    (isError && [
      error?.non_field_errors ||
        "Le formulaire contient des erreurs. Corrigez-les et ré-essayez.",
    ]) ||
    [];

  return enabled ? (
    <Container maxWidth="md" disableGutters>
      <Stack sx={{ width: "100%", m: "auto", p: { xs: 1, md: 3 } }}>
        <Typography component="h2" variant="h4" color="primary" sx={{ p: 2 }}>
          {title}
          {isLoading && <CircularProgress sx={{ m: 2, mb: 0 }} size={20} />}
        </Typography>
        <ErrorBox errorList={get_error_message()} />
        <FormComponent
          data={data || defaultData}
          status={status || {}}
          has_all_access={has_all_access}
          onSubmit={handleSubmit}
        />
        {children}
      </Stack>
      <GenericSaveSuccessDialog
        mutation_request={request}
        form_key={formKey}
        detail_route={showRoute}
        disabled={false}
        onDialogClose={redirectAction}
      />
    </Container>
  ) : (
    <ErrorBox errorList={["Ce formulaire n'est pas disponible"]} />
  );
}
