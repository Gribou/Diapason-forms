import React from "react";
import { Part, Row, Cell } from "components/misc/PageElements";
import FormDateTimeField from "components/forms/fields/FormDateTimeField";

export default function Form({ formProps, ...props }) {
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
      </Row>
    </Part>
  );
}
