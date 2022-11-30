import React, { useEffect, Fragment } from "react";
import { useParams } from "react-router-dom";
import { Container, Box } from "@mui/material";
import { useMe, useAuthenticated } from "features/auth/hooks";
import { useFormConfig } from "features/config/hooks";
import formMappings, { useFormByUUID } from "features/forms/mappings";
import { useSearchParams } from "features/router";

import ErrorBox from "components/misc/ErrorBox";
import { scrollToTop } from "features/ui";
import GenericSaveSuccessDialog from "../GenericSaveSuccessDialog";
import useShowFormHeader from "./Header";

const useShowFormStatus = (pk, formKey) => {
  const [params] = useSearchParams();
  const { is_validator } = useMe();
  const query = useFormByUUID(formKey, pk, params);
  const { data, refetch, ...status } = query;
  const [update, updateRequest] = formMappings[formKey].update();

  const draftMode = Boolean(!data?.status || data?.status?.is_draft);
  const validatorMode = Boolean(
    is_validator && data?.assigned_to_group?.permissions?.includes("validator")
  );

  const isAnythingLoading = status?.isFetching || updateRequest?.isLoading;

  return {
    draftMode,
    validatorMode,
    isAnythingLoading,
    query: {
      ...query,
      status: updateRequest?.isUninitialized ? status : updateRequest,
      refetch,
    },
    reset: updateRequest?.reset,
    update,
    mutation_status: updateRequest,
  };
};

export default function ShowFormPage({
  formKey,
  title,
  showRoute,
  DisplayComponent,
  FormComponent,
  children,
}) {
  const { pk } = useParams();
  const { enabled } = useFormConfig(formKey);
  const {
    query,
    draftMode,
    validatorMode,
    isAnythingLoading,
    update,
    reset,
    mutation_status,
  } = useShowFormStatus(pk, formKey);
  const is_authenticated = useAuthenticated();
  const header = useShowFormHeader({
    formKey,
    loading: isAnythingLoading,
    title,
    query,
    showRoute,
  });

  useEffect(() => {
    header?.edit?.reset();
    reset(); //set state to uninitialized
  }, [pk]);

  const onCancel = () => {
    scrollToTop();
    header?.edit.reset();
  };

  //show dialogs depending on options then apply submit function
  //proceed : should default next action be applied
  //bypass_validation : should form be auto validated (cf actions/forms.js)
  const handleSubmit = (form, options) => {
    update({ ...form, is_authenticated, options });
    scrollToTop();
    header?.edit.reset();
  };

  const show_form = Boolean(
    query?.data?.event_date &&
      ((draftMode && !query?.data?.readOnly) ||
        validatorMode ||
        header?.edit.value ||
        mutation_status?.isError)
  );

  const show_display = Boolean(query?.data?.event_date);

  return enabled ? (
    <Container maxWidth="md" disableGutters>
      <Box sx={{ width: "100%", m: "auto", p: { xs: 1, md: 3 } }}>
        {header.display}

        {/* show only if found (not found = no event_date)*/}
        {/* show form if draft or cds or edit_mode or has_errors, else display data read only*/}
        {/* if error, show submitted data that triggered error (and not only the original data from query so that user does not have to re-fill all fields)*/}
        {show_form ? (
          <FormComponent
            data={{
              ...query?.data,
              ...(mutation_status?.isError
                ? mutation_status?.originalArgs
                : {}),
            }}
            status={
              mutation_status?.isError || mutation_status?.isLoading
                ? mutation_status
                : query?.status
            }
            validatorMode={validatorMode}
            investigatorMode={header?.edit.value}
            onSubmit={handleSubmit}
            onCancel={onCancel}
          />
        ) : show_display ? (
          <Fragment>
            {!query?.data?.readOnly && <ErrorBox errorDict={status?.error} />}
            <DisplayComponent
              data={query?.data}
              anonymous={header?.anonymous}
            />
          </Fragment>
        ) : (
          <ErrorBox errorDict={query?.status?.error} />
        )}
      </Box>
      {children}
      <GenericSaveSuccessDialog
        mutation_request={mutation_status}
        form_key={formKey}
        detail_route={showRoute}
      />
    </Container>
  ) : (
    <ErrorBox errorList={["Ce formulaire n'est pas disponible"]} />
  );
}
