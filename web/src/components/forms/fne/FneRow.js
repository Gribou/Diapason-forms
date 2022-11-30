import React from "react";
import { Shape, Airplane } from "mdi-material-ui";

import { ROUTES } from "routes";
import FormListRow, {
  ErrorChip,
  NormalChip,
  WarningChip,
} from "components/forms/generic/FormListRow";
import formMappings, { FNE_FORM_KEY } from "features/forms/mappings";
import { useFormConfig } from "features/config/hooks";

export default function FneRow({ data, ...props }) {
  const {
    event_types,
    tcas_report,
    sub_data,
    has_warning,
    has_alarm,
    safetycube,
  } = data || {};
  const { safetycube_enabled } = useFormConfig(FNE_FORM_KEY);
  const [update, { isLoading }] = formMappings[FNE_FORM_KEY].update();

  const acknowledgeWarning = (e) => {
    e.stopPropagation();
    update({
      ...data,
      is_authenticated: true,
      sub_data: {
        ...(sub_data || {}),
        alarm_acknowledged: !sub_data?.alarm_acknowledged,
      },
    });
  };

  const aircraft_list = [
    ...new Set(
      [...(data?.aircrafts || []), ...(data?.tcas_report?.aircrafts || [])]
        ?.filter(({ callsign }) => callsign)
        ?.map(({ callsign }) => callsign)
    ),
  ].join(" ");

  const type_display = event_types
    ?.filter(({ is_tcas }) => !is_tcas)
    ?.map(({ name }) => name)
    .join(" ");

  return (
    <FormListRow
      data={data}
      detailRoute={ROUTES.show_fne}
      subtitle={
        safetycube_enabled
          ? safetycube?.reference || "Non enregistré SafetyCube"
          : sub_data?.inca_number?.toUpperCase() || "INCA"
      }
      loading={isLoading}
      form_key={FNE_FORM_KEY}
      {...props}
    >
      {has_alarm && (
        <ErrorChip
          label={`${has_alarm}j`}
          variant={sub_data?.alarm_acknowledged ? "outlined" : "default"}
          clickable
          onClick={acknowledgeWarning}
        />
      )}
      {has_warning && (
        <WarningChip
          label={`${has_warning}j`}
          variant={sub_data?.alarm_acknowledged ? "outlined" : "default"}
          onClick={acknowledgeWarning}
        />
      )}
      {tcas_report && <ErrorChip label="TCAS" />}
      {sub_data?.hn && <ErrorChip label={sub_data?.hn} />}
      {type_display && (
        <NormalChip IconComponent={Shape} label={type_display} />
      )}
      {aircraft_list && (
        <NormalChip IconComponent={Airplane} label={aircraft_list} />
      )}
    </FormListRow>
  );
}
