import React from "react";
import { Alert } from "@mui/material";
import { Part, Row, Cell } from "components/misc/PageElements";
import { YES_NO_CHOICES } from "constants/config";
import {
  FormCheckboxGroupField,
  FormTextField,
  FormRadioField,
} from "components/forms/fields";
import { useInterferenceTypes } from "features/config/hooks";

export default function Form({ formProps, ...props }) {
  const interferenceTypes = useInterferenceTypes();

  return (
    <Part title="Description de l'évènement" defaultExpanded {...props}>
      <Row>
        <Cell span>
          <FormCheckboxGroupField
            id="interferences"
            label="Type(s) d'interférences"
            choices={interferenceTypes}
            {...formProps}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <FormRadioField
            id="freq_unusable"
            label="Fréquence inutilisable :"
            choices={YES_NO_CHOICES}
            boolean
            sx={{
              flexDirection: "row",
              alignItems: "center",
              justifyContent: "space-between",
            }}
            legendComponent="span"
            legendSx={{ mr: 1 }}
            {...formProps}
          />
        </Cell>
        <Cell span>
          <FormRadioField
            id="traffic_impact"
            label="Impact sur le trafic :"
            choices={YES_NO_CHOICES}
            boolean
            sx={{
              flexDirection: "row",
              alignItems: "center",
              justifyContent: "space-between",
            }}
            legendComponent="span"
            legendSx={{ mr: 1 }}
            {...formProps}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={6}>
          <FormRadioField
            id="supp_freq"
            label="Fréquence supplétive utilisée :"
            choices={YES_NO_CHOICES}
            boolean
            sx={{
              flexDirection: "row",
              alignItems: "center",
              justifyContent: "space-between",
            }}
            legendComponent="span"
            legendSx={{ mr: 1 }}
            {...formProps}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={12}>
          <FormTextField
            multiline
            required
            rows={6}
            id="description"
            label="Commentaire"
            {...formProps}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Alert severity="info">
            Si vous avez reçu des paroles ou une autre fréquence ATC, indiquez
            aussi précisément que possible le contenu du/des messages reçus.
          </Alert>
        </Cell>
      </Row>
    </Part>
  );
}
