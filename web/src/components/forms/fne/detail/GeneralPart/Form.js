import React from "react";
import { Part, Row, Cell } from "components/misc/PageElements";
import {
  useSectors,
  usePositions,
  useSectorGroups,
  useRoles,
} from "features/config/hooks";
import {
  FormTextField,
  FormDateTimeField,
  FormCheckboxField,
  FormSelectField,
} from "components/forms/fields";

export default function Form({ formProps, ...props }) {
  const sectors = useSectors();
  const positions = usePositions();
  const sector_groups = useSectorGroups();
  const roles = useRoles();
  const { values, onChange } = formProps;

  const handleIspChange = (event) => {
    const { value: checked } = event.target;
    //add ECR/ECO redactors if do not exist and ISP is checked
    //only if ECR/ECO exist in roles list (CAUTRA mode probably)
    if (
      checked &&
      roles?.includes("ECO") &&
      roles?.includes("ECR") &&
      !values?.redactors?.some(({ role }) => role === "ECR" || role === "ECO")
    ) {
      onChange([
        event,
        {
          target: {
            name: "redactors",
            value: [
              ...(values?.redactors || []),
              { role: "ECR" },
              { role: "ECO" },
            ],
          },
        },
      ]);
    } else {
      onChange({ target: { name: "isp", value: checked } });
    }
  };

  return (
    <Part title="Informations générales" defaultExpanded {...props}>
      <Row>
        <Cell span={5} direction="column" alignItems="stretch">
          <FormDateTimeField
            id="event_date"
            required
            warnIfOlderThanHours={2}
            label="Date et heure (TU)"
            {...formProps}
          />
        </Cell>
        <Cell span />
        <Cell alignItems="stretch">
          <FormCheckboxField
            id="isp"
            label="Instruction sur Position"
            {...formProps}
            onChange={handleIspChange}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={4}>
          <FormSelectField
            id="secteur"
            label="Secteur"
            {...formProps}
            freeSolo
            choices={sectors}
          />
        </Cell>
        <Cell span={4}>
          <FormSelectField
            id="position"
            label="Position"
            required
            {...formProps}
            choices={positions}
            freeSolo
          />
        </Cell>
        <Cell span={4}>
          <FormSelectField
            id="regroupement"
            label="Regroupement"
            required
            {...formProps}
            choices={sector_groups}
            freeSolo
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={12}>
          <FormTextField id="lieu" label="Lieu de l'évènement" {...formProps} />
        </Cell>
      </Row>
    </Part>
  );
}
