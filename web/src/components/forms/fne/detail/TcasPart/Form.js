import React from "react";
import { Typography, InputAdornment, Button } from "@mui/material";
import { Plus } from "mdi-material-ui";

import {
  FLOAT_PATTERN,
  INTEGER_PATTERN,
  YES_NO_CHOICES,
} from "constants/config";
import { Part, Row, Cell, DividerRow } from "components/misc/PageElements";
import { FormRadioField, FormTextField } from "components/forms/fields";
import AircraftSubForm from "./AircraftSubForm";

export default function Form({ formProps, ...props }) {
  const { values, touched, errors, onChange } = formProps;

  const handleChange = (event) =>
    onChange({
      target: {
        name: "tcas_report",
        value: {
          ...(values?.tcas_report || {}),
          [event.target.name]: event.target.value,
        },
      },
    });

  const handleAdd = () =>
    onChange({
      target: {
        name: "tcas_report",
        value: {
          ...(values?.tcas_report || {}),
          aircrafts: [...(values?.tcas_report?.aircrafts || []), {}],
        },
      },
    });

  const form_props = {
    values: values?.tcas_report || {},
    errors: errors?.tcas_report || {},
    touched: touched?.tcas_report || {},
    onChange: (e) => handleChange(e),
  };

  return (
    <Part
      title="Compte-rendu d'évènement TCAS"
      defaultExpanded
      addOn={
        <Button
          size="small"
          color="primary"
          startIcon={<Plus />}
          variant="outlined"
          onFocus={(e) => e.stopPropagation()}
          onClick={(e) => {
            e.stopPropagation();
            handleAdd();
          }}
        >
          Ajouter Aéronef
        </Button>
      }
      {...props}
    >
      {values?.tcas_report?.aircrafts?.map((a, i) => (
        <AircraftSubForm
          index={i}
          key={i}
          {...form_props}
          values={values}
          onChange={onChange}
        />
      ))}
      <Row>
        <Cell span={4} direction="column">
          <Typography variant="overline" color="textSecondary">
            Analyse pilote
          </Typography>
          <Typography variant="caption" color="textSecondary"></Typography>
        </Cell>
        <Cell span={4}>
          <FormTextField
            fullWidth
            label="Distance minimale"
            id="pilote_min_distance"
            inputProps={{
              inputMode: "numeric",
            }}
            pattern={FLOAT_PATTERN}
            InputProps={{
              endAdornment: <InputAdornment position="end">NM</InputAdornment>,
            }}
            {...form_props}
          />
        </Cell>
        <Cell span={4}>
          <FormTextField
            fullWidth
            id="pilote_min_altitude"
            label="Altitude minimale"
            inputProps={{
              inputMode: "numeric",
            }}
            pattern={INTEGER_PATTERN}
            InputProps={{
              endAdornment: <InputAdornment position="end">ft</InputAdornment>,
            }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span={4} direction="column">
          <Typography variant="overline" color="textSecondary">
            Analyse contrôleur
          </Typography>
          <Typography variant="caption" color="textSecondary"></Typography>
        </Cell>
        <Cell span={4}>
          <FormTextField
            fullWidth
            label="Distance minimale"
            id="ctl_min_distance"
            inputProps={{
              inputMode: "numeric",
            }}
            pattern={FLOAT_PATTERN}
            InputProps={{
              endAdornment: <InputAdornment position="end">NM</InputAdornment>,
            }}
            {...form_props}
          />
        </Cell>
        <Cell span={4}>
          <FormTextField
            fullWidth
            label="Altitude minimale"
            id="ctl_min_altitude"
            inputProps={{
              inputMode: "numeric",
            }}
            pattern={INTEGER_PATTERN}
            InputProps={{
              endAdornment: <InputAdornment position="end">ft</InputAdornment>,
            }}
            {...form_props}
          />
        </Cell>
      </Row>
      <DividerRow />
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            Y a-t-il eu une information de trafic ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="traffic_info"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">Sur demande du pilote ?</Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="pilot_request"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            Si OUI, la demande a-t-elle été faite avant ou après la manoeuvre ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="before_manoeuvre"
            choices={[
              { label: "Avant", value: true },
              { label: "Après", value: false },
            ]}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            A votre avis, l&apos;action du pilote était-elle justifiée ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="pilot_action_required"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            Cet évènement a-t-il perturbé votre gestion du trafic ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="disrupted_traffic"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            L&apos;un des pilotes a-t-il signalé vouloir rédiger un ASR ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="asr"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
      <Row>
        <Cell span>
          <Typography color="textSecondary">
            Le filet de sauvegarde s&apos;est-il déclenché ?
          </Typography>
        </Cell>
        <Cell span={3}>
          <FormRadioField
            id="safety_net"
            choices={YES_NO_CHOICES}
            boolean
            radioSx={{ flex: "1 1 0%", mr: 0 }}
            {...form_props}
          />
        </Cell>
      </Row>
    </Part>
  );
}
