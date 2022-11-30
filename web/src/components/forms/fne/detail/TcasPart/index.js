import React from "react";

import Form from "./Form";
import Display from "./Display";
import GenericDetail from "components/forms/generic/detail/GenericDetail";
export { NEW_TCAS_REPORT } from "./AircraftSubForm";

export default function CdsPart(props) {
  return (
    <GenericDetail FormComponent={Form} DisplayComponent={Display} {...props} />
  );
}
