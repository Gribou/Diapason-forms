import React from "react";
import { Part, Row, Cell } from "components/misc/PageElements";
import FormTextField from "components/forms/fields/FormTextField";
import FormCheckboxField from "components/forms/fields/FormCheckboxField";

export default function Form({ formProps, ...props }) {
  const { values, errors, touched, onChange } = formProps;

  const handleChange = (event) =>
    onChange({
      target: {
        name: "cds_report",
        value: {
          ...(values?.cds_report || {}),
          [event.target.name]: event.target.value,
        },
      },
    });

  const form_props = {
    values: values?.cds_report || {},
    errors: errors?.cds_report || {},
    touched: touched?.cds_report || {},
    onChange: handleChange,
  };

  return (
    <Part title="Chef de Salle" defaultExpanded {...props}>
      <Row>
        <Cell span={4} alignItems="flex-end">
          <FormCheckboxField
            id="notif_rpo"
            label="Notification RPO"
            {...form_props}
          />
        </Cell>
        <Cell span={4} alignItems="flex-end">
          <FormCheckboxField
            id="cpi"
            label="Constat Préalable d'Infraction"
            {...form_props}
          />
        </Cell>
        <Cell span={4} alignItems="flex-end">
          <FormCheckboxField
            id="rex_cds"
            label="REX Chef de Salle"
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={12}>
          <FormTextField
            multiline
            rows={6}
            id="com_cds"
            label="Commentaire"
            {...form_props}
          />
        </Cell>
      </Row>
    </Part>
  );
}
