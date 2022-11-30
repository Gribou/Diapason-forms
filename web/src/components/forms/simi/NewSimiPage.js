import React from "react";
import { SIMI_FORM_KEY } from "features/forms/mappings";
import SimiForm from "components/forms/simi/SimiForm";
import { ROUTES } from "routes";
import NewFormPage from "components/forms/generic/NewFormPage";

const DEFAULT_SIMI = {
  redactors: [{}],
  aircrafts: [{}, {}],
};

export default function NewSimiPage() {
  return (
    <NewFormPage
      title="Nouvelle Fiche Similitude d'Indicatifs"
      formKey={SIMI_FORM_KEY}
      defaultData={DEFAULT_SIMI}
      showRoute={ROUTES.show_simi}
      FormComponent={SimiForm}
    />
  );
}
