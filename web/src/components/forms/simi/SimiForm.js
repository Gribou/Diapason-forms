import React from "react";
import { useForm } from "features/ui";
import GenericForm from "components/forms/generic/GenericForm";
import { GeneralPart, AircraftsPart, DescriptionPart } from "./detail";
import { RedactorsPart } from "components/forms/generic/detail";
import usePreSubmitChecks from "components/forms/generic/GenericForm/PreSubmitChecks";
import { SIMI_FORM_KEY } from "features/forms/mappings";

const useSimiFormProps = (props) => {
  const { status, data, validatorMode, onSubmit } = props;
  const { error } = status || {};
  const { values, touched, handleUserInput, handleSubmit } = useForm(
    {
      ...(data || {}),
      redactors: [...(data?.redactors || []), ...(validatorMode ? [{}] : [])],
    },
    onSubmit
  );

  return {
    values,
    touched,
    errors: error || {},
    onChange: handleUserInput,
    onSubmit: handleSubmit,
  };
};

export default function SimiForm(props) {
  const form_props = useSimiFormProps(props);
  const { data, validatorMode } = props;
  const preSubmitChecks = usePreSubmitChecks(form_props);

  return (
    <GenericForm
      {...props}
      onSubmit={preSubmitChecks.check}
      formKey={SIMI_FORM_KEY}
    >
      <GeneralPart
        formProps={form_props}
        data={data}
        editMode={!validatorMode}
      />
      <RedactorsPart editMode formProps={form_props} data={data} />
      <AircraftsPart
        editMode={!validatorMode}
        data={data}
        formProps={form_props}
      />
      <DescriptionPart
        formProps={form_props}
        editMode={!validatorMode}
        data={data}
      />
      {preSubmitChecks.display}
    </GenericForm>
  );
}
