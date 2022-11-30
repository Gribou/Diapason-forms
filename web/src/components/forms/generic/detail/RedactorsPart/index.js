import React from "react";
import GenericMultiRowDetail from "components/forms/generic/detail/GenericMultiRowDetail";
import { useTeams, useRoles } from "features/config/hooks";
import RedactorRow from "./RowDisplay";
import RedactorSubForm from "./RowForm";

export default function RedactorsPart({ data, showRole, ...props }) {
  const teams = useTeams();
  const roles = useRoles();

  return (
    <GenericMultiRowDetail
      item_name="Rédacteur"
      item_key="redactors"
      items={data?.redactors}
      SubDisplayComponent={RedactorRow}
      additionalDisplayProps={{
        empty_text: "Aucun rédacteur",
        rowProps: { showRole },
      }}
      SubFormComponent={RedactorSubForm}
      additionalFormProps={{ rowProps: { teams, roles, showRole } }}
      {...props}
    />
  );
}
