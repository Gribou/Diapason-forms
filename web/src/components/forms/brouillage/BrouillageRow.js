import React from "react";
import { Antenna } from "mdi-material-ui";
import FormListRow, { NormalChip } from "components/forms/generic/FormListRow";
import { ROUTES } from "routes";
import { BROUILLAGE_FORM_KEY } from "features/forms/mappings";

export default function BrouillageRow({ data, ...props }) {
  const { frequency } = data || {};
  return (
    <FormListRow
      data={data}
      detailRoute={ROUTES.show_brouillage}
      form_key={BROUILLAGE_FORM_KEY}
      {...props}
    >
      {frequency && <NormalChip IconComponent={Antenna} label={frequency} />}
    </FormListRow>
  );
}
