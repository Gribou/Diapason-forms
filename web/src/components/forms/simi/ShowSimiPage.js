import React from "react";

import { SIMI_FORM_KEY } from "features/forms/mappings";
import { ROUTES } from "routes";

import SimiDisplay from "components/forms/simi/SimiDisplay";
import SimiForm from "components/forms/simi/SimiForm";
import ShowFormPage from "components/forms/generic/ShowFormPage";

export default function ShowSimiPage() {

  return (
    <ShowFormPage
      formKey={SIMI_FORM_KEY}
      title="Fiche Similitude d'Indicatifs"
      DisplayComponent={SimiDisplay}
      FormComponent={SimiForm}
      showRoute={ROUTES.show_simi}
    />
  );
}
