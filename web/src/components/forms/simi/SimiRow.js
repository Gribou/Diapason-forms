import React from "react";
import { Airplane } from "mdi-material-ui";

import FormListRow, { NormalChip } from "components/forms/generic/FormListRow";
import { ROUTES } from "routes";
import { SIMI_FORM_KEY } from "features/forms/mappings";
import { useFormConfig } from "features/config/hooks";

export default function SimiRow({ data, ...props }) {
  const { sub_data, safetycube } = data || {};
  const { safetycube_enabled } = useFormConfig(SIMI_FORM_KEY);

  const aircraft_list = [
    ...new Set(
      (data?.aircrafts || [])
        ?.filter(({ callsign }) => callsign)
        ?.map(({ callsign }) => callsign)
    ),
  ].join(" ");

  return (
    <FormListRow
      data={data}
      detailRoute={ROUTES.show_simi}
      subtitle={
        safetycube_enabled
          ? safetycube?.reference || "Non enregistré SafetyCube"
          : sub_data?.inca_number?.toUpperCase() || "INCA"
      }
      noAvatar
      form_key={SIMI_FORM_KEY}
      {...props}
    >
      {aircraft_list && (
        <NormalChip IconComponent={Airplane} label={aircraft_list} />
      )}
    </FormListRow>
  );
}
