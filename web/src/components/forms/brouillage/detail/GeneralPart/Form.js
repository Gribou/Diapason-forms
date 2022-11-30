import React from "react";
import { Part, Row, Cell } from "components/misc/PageElements";
import {
  FormDateTimeField,
  FormTextField,
  FormSelectField,
} from "components/forms/fields";
import { usePositions } from "features/config/hooks";

export default function Form({ formProps, ...props }) {
  const positions = usePositions();
  return (
    <Part title="Informations générales" defaultExpanded {...props}>
      <Row>
        <Cell span={5} direction="column" alignItems="stretch">
          <FormDateTimeField
            id="event_date"
            required
            label="Date et heure (TU)"
            warnIfOlderThanHours={2}
            {...formProps}
          />
        </Cell>
        <Cell span={1} />
        <Cell span alignItems="flex-start">
          <FormTextField
            id="frequency"
            required
            label="Fréquence(s)"
            {...formProps}
          />
        </Cell>
        <Cell span alignItems="flex-start">
          <FormSelectField
            id="cwp"
            label="Position de contrôle"
            {...formProps}
            choices={positions}
            freeSolo
          />
        </Cell>
      </Row>
    </Part>
  );
}
