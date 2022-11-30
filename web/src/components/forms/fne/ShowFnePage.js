import React from "react";

import FneDisplay from "./FneDisplay";
import FneForm from "./FneForm";
import ShowFormPage from "components/forms/generic/ShowFormPage";
import { FNE_FORM_KEY } from "features/forms/mappings";
import { ROUTES } from "routes";

export default function ShowFnePage() {
  return (
    <ShowFormPage
      formKey={FNE_FORM_KEY}
      title="Fiche de Notification d'Evènement"
      DisplayComponent={FneDisplay}
      FormComponent={FneForm}
      showRoute={ROUTES.show_fne}
    />
  );
}
