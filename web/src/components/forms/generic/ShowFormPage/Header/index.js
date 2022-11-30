import React from "react";
import { Stack, Typography } from "@mui/material";
import { useMe } from "features/auth/hooks";
import useAnonymousButton from "./AnonymousButton";
import useEditButton from "./EditButton";
import PreviousButton from "./PreviousButton";
import NextButton from "./NextButton";
import BackToListButton from "./BackToListButton";
import RefreshButton from "components/misc/RefreshButton";
import StatusButton from "components/forms/generic/StatusButton";

export default function ShowFormHeader({
  formKey,
  loading,
  title,
  query,
  showRoute,
}) {
  const { is_validator, is_investigator, has_all_access } = useMe();
  const { data, refetch, ...status } = query;
  const next = (is_validator || is_investigator) && data?.next_form;
  const prev = (is_validator || is_investigator) && data?.previous_form;

  const anonymous = useAnonymousButton();
  const edit = useEditButton();
  const status_button = data && is_investigator && (
    <StatusButton
      form={data}
      loading={loading}
      status={status}
      form_key={formKey}
    />
  );

  const display = (
    <Stack direction="row" sx={{ mb: 2 }}>
      <Typography
        component="h2"
        variant="h4"
        color="primary"
        sx={{ mr: 2, flexGrow: 1 }}
      >
        {title}
      </Typography>

      <Stack alignItems="flex-end">
        {status_button}
        <Stack direction="row" justifyContent="flex-end" sx={{ mt: 1 }}>
          <RefreshButton loading={loading} refresh={refetch} key="refresh" />
          {has_all_access && !edit?.value && edit.display}
          {data && is_investigator && anonymous.display}
          {prev && <PreviousButton uuid={prev} route={showRoute} />}
          {next && <NextButton uuid={next} route={showRoute} />}
          {(is_validator || is_investigator) && <BackToListButton />}
        </Stack>
      </Stack>
    </Stack>
  );

  return { display, anonymous: anonymous.value, edit };
}
