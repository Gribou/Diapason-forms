import React from "react";

import { BROUILLAGE_FORM_KEY } from "features/forms/mappings";
import { ROUTES } from "routes";

import NewFormPage from "components/forms/generic/NewFormPage";
import BrouillageForm from "./BrouillageForm";

const DEFAULT_BROUILLAGE = {
  redactors: [{}],
  aircrafts: [{}],
};

export default function NewBrouillagePage() {
  return (
    <NewFormPage
      title="Nouvelle Fiche Brouillage"
      formKey={BROUILLAGE_FORM_KEY}
      defaultData={DEFAULT_BROUILLAGE}
      showRoute={ROUTES.show_brouillage}
      FormComponent={BrouillageForm}
    />
  );
}
