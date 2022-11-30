import React, { useEffect } from "react";
import { useForm } from "features/ui";
import { FNE_FORM_KEY } from "features/forms/mappings";
import { useMe } from "features/auth/hooks";
import GenericForm from "components/forms/generic/GenericForm";
import {
  GeneralPart,
  DescriptionPart,
  CdsPart,
  TcasPart,
  AircraftsPart,
} from "../detail";
import { RedactorsPart, AttachmentPart } from "components/forms/generic/detail";
import useFnePreSubmitChecks from "./FnePreSubmitChecks";

const useFneFormProps = (props) => {
  const { status, data, validatorMode, investigatorMode, onSubmit } = props;
  const { error } = status || {};
  const { values, touched, handleUserInput, handleSubmit, reset } = useForm(
    {
      ...(data || {}),
      redactors: [
        ...(data?.redactors || []),
        ...(validatorMode &&
        !data?.redactors?.find(({ role }) => role === "CDS")
          ? [{ role: "CDS" }]
          : []),
      ],
    },
    onSubmit
  );

  useEffect(() => {
    reset({
      ...(data || {}),
      redactors: [
        ...(data?.redactors || []),
        ...(validatorMode &&
        !data?.redactors?.find(({ role }) => role === "CDS")
          ? [{ role: "CDS" }]
          : []),
      ],
    });
  }, [data]);

  return {
    is_tcas_event: Boolean(values.event_types?.some(({ is_tcas }) => is_tcas)),
    draftMode: !validatorMode && !investigatorMode,
    form_props: {
      values,
      touched,
      errors: error || {},
      onChange: handleUserInput,
      onSubmit: handleSubmit,
    },
  };
};

export default function FneForm(props) {
  const me = useMe();
  const { data, validatorMode } = props;
  const { form_props, is_tcas_event, draftMode } = useFneFormProps(props);
  const preSubmitChecks = useFnePreSubmitChecks(form_props);

  return (
    <GenericForm
      {...props}
      onSubmit={preSubmitChecks.check}
      formKey={FNE_FORM_KEY}
    >
      <GeneralPart
        formProps={form_props}
        data={data}
        editMode={!validatorMode}
      />
      <RedactorsPart editMode showRole formProps={form_props} data={data} />
      <AircraftsPart
        editMode={!validatorMode}
        data={data}
        formProps={form_props}
      />
      <DescriptionPart formProps={form_props} editMode data={data} />
      {is_tcas_event && (
        <TcasPart
          data={data}
          formProps={form_props}
          editMode={!validatorMode}
        />
      )}
      {(!draftMode || me?.is_validator) && (
        <CdsPart editMode data={data} formProps={form_props} />
      )}
      <AttachmentPart
        data={data}
        formProps={form_props}
        form_key={FNE_FORM_KEY}
        defaultExpanded
      />
      {preSubmitChecks.display}
    </GenericForm>
  );
}
