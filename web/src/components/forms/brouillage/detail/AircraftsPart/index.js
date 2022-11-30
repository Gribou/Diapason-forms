import React from "react";

import GenericMultiRowDetail from "components/forms/generic/detail/GenericMultiRowDetail";
import AircraftRow from "./RowDisplay";
import AircraftForm from "./RowForm";

export default function AircraftsPart({ data, ...props }) {
  return (
    <GenericMultiRowDetail
      item_name="Aéronef"
      item_key="aircrafts"
      items={data?.aircrafts}
      SubDisplayComponent={AircraftRow}
      additionalDisplayProps={{
        empty_text: "Aucun aéronef",
      }}
      SubFormComponent={AircraftForm}
      {...props}
    />
  );
}
