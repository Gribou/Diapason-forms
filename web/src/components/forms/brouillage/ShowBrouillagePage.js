import React from "react";

import { BROUILLAGE_FORM_KEY } from "features/forms/mappings";
import { ROUTES } from "routes";

import BrouillageDisplay from "./BrouillageDisplay";
import BrouillageForm from "./BrouillageForm";
import ShowFormPage from "components/forms/generic/ShowFormPage";

export default function ShowBrouillagePage() {
  return (
    <ShowFormPage
      formKey={BROUILLAGE_FORM_KEY}
      title="Fiche Brouillage"
      DisplayComponent={BrouillageDisplay}
      FormComponent={BrouillageForm}
      showRoute={ROUTES.show_brouillage}
    />
  );
}
