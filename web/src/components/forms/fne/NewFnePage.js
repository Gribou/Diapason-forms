import React from "react";
import { useFeatures, useRoles } from "features/config/hooks";
import { FNE_FORM_KEY } from "features/forms/mappings";
import { ROUTES } from "routes";
import FneForm from "./FneForm";
import NewFormPage from "components/forms/generic/NewFormPage";

const make_default_fne = (atco_mode, roles) => {
  //TODO 3E ?
  if (
    atco_mode === "CAUTRA" &&
    roles?.includes("PCR") &&
    roles?.includes("PCO")
  ) {
    return {
      redactors: [{ role: "PCR" }, { role: "PCO" }],
      aircrafts: [{}],
    };
  }
  if (
    atco_mode === "4F" &&
    roles?.includes("Tactical") &&
    roles?.includes("Planner")
  ) {
    return {
      redactors: [{ role: "Tactical" }, { role: "Planner" }],
      aircrafts: [{}],
    };
  }
  return {
    redactors: [{}, {}],
    aircrafts: [{}],
  };
};

export default function NewFnePage() {
  const { atco_mode } = useFeatures();
  const roles = useRoles();
  return (
    <NewFormPage
      title="Nouvelle Fiche de Notification d'Evènement"
      formKey={FNE_FORM_KEY}
      defaultData={make_default_fne(atco_mode, roles)}
      FormComponent={FneForm}
      showRoute={ROUTES.show_fne}
    />
  );
}
