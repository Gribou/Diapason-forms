import React from "react";
import { Typography, Box, Alert } from "@mui/material";

import { useEventTypes, useTechEventTypes } from "features/config/hooks";

import { Part, Row, Cell } from "components/misc/PageElements";
import {
  DrawingField,
  FormTextField,
  FormCheckboxGroupField,
} from "components/forms/fields";
import { makeTechActionsToDo } from "../../utils";

import { NEW_TCAS_REPORT } from "../TcasPart";

export default function Form({ formProps, ...props }) {
  const eventTypes = useEventTypes();
  const techEventTypes = useTechEventTypes();
  const { values, onChange } = formProps;

  const tech_actions_to_do = makeTechActionsToDo(values);

  const onEventTypeChange = (event) => {
    const is_tcas_event = event.target.value?.find(({ is_tcas }) => is_tcas);
    //Tech event types that have the same name as the event type
    const tech_events = techEventTypes?.filter(({ name }) =>
      event.target.value?.map((event) => event?.name)?.includes(name)
    );
    let events = [event];
    if (is_tcas_event) {
      // add pre-populated tcas_report if it is not present
      events = [
        ...events,
        {
          target: {
            name: "tcas_report",
            value: {
              ...NEW_TCAS_REPORT,
              ...values?.tcas_report,
            },
          },
        },
      ];
    }
    if (tech_events) {
      events = [
        ...events,
        {
          target: {
            name: "tech_event",
            value: [...(values?.tech_event || []), ...tech_events],
          },
        },
      ];
    }
    //do not delete tcas_report or tech event if event type is unchecked (in case user changes opinion)
    onChange(events);
  };

  return (
    <Part title="Description de l'évènement" defaultExpanded {...props}>
      <Row>
        <Cell span={12}>
          <FormCheckboxGroupField
            id="event_types"
            label="Type(s) d'évènement"
            choices={eventTypes}
            {...formProps}
            onChange={onEventTypeChange}
          />
        </Cell>
      </Row>
      <Row sx={{ mt: 1 }}>
        <Cell span>
          <FormCheckboxGroupField
            id="tech_event"
            label="Evènement technique"
            choices={techEventTypes}
            getOptionLabel={(choice) => choice?.helperText || choice?.name}
            {...formProps}
          />
        </Cell>
      </Row>
      {tech_actions_to_do?.length > 0 && (
        <Row>
          <Cell span>
            <Box
              sx={{
                border: 1,
                borderRadius: 5,
                borderColor: "error.main",
                mx: 1,
                my: 2,
                px: 2,
                py: 1,
              }}
            >
              <Typography variant="overline" color="error">
                Actions à entreprendre
              </Typography>
              <FormCheckboxGroupField
                id="tech_actions_done"
                choices={tech_actions_to_do}
                getOptionLabel={(choice) => choice?.name}
                getOptionHelperText={(choice) => choice?.helperText}
                {...formProps}
              />
              <Typography variant="caption" color="error">
                Cochez les cases ci-dessus après avoir effectué l&apos;action
                correspondante.
              </Typography>
            </Box>
          </Cell>
        </Row>
      )}
      <Row sx={{ mt: 1 }}>
        <Cell span={12}>
          <FormTextField
            multiline
            required
            rows={6}
            id="description"
            label="Description"
            {...formProps}
          />
        </Cell>
      </Row>
      <Row>
        <Cell>
          <DrawingField label="Schéma descriptif" id="drawing" {...formProps} />
        </Cell>
      </Row>
      <Row>
        <Cell>
          <Alert severity="info">
            Si vous estimez que la fatigue, le stress ou la prise de substances
            psychoactives ont pu jouer un rôle dans cet évènement, vous pouvez
            vous rapprocher de l&apos;entité QS/S.
          </Alert>
        </Cell>
      </Row>
    </Part>
  );
}
