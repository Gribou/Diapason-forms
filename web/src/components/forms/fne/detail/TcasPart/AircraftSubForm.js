import React from "react";
import { Typography, InputAdornment, Box, IconButton } from "@mui/material";
import { Delete } from "mdi-material-ui";

import { FL_PATTERN, SSR_PATTERN, YES_NO_CHOICES } from "constants/config";
import { TCAS_TYPES, FLIGHT_PHASES } from "constants/fne";
import { Row, Cell } from "components/misc/PageElements";
import {
  FormRadioField,
  FormTextField,
  FormSelectField,
} from "components/forms/fields";

export const NEW_TCAS_REPORT = {
  aircrafts: [{ is_origin: true }, {}],
};

export default function TcasAircraftSubForm({
  index,
  values,
  errors,
  touched,
  onChange,
}) {
  const handleChange = (event, field_name) => {
    const new_aircrafts = (values?.tcas_report?.aircrafts || []).map((a, i) =>
      i === index ? { ...a, [field_name]: event.target.value } : a
    );
    onChange({
      target: {
        name: "tcas_report",
        value: { ...values.tcas_report, aircrafts: new_aircrafts },
      },
    });
  };

  const handleDelete = () => {
    const new_aircrafts = (values?.tcas_report?.aircrafts || []).filter(
      (a, i) => i !== index
    );
    onChange({
      target: {
        name: "tcas_report",
        value: { ...values.tcas_report, aircrafts: new_aircrafts },
      },
    });
  };

  const form_props = {
    values: values?.tcas_report?.aircrafts[index] || {},
    errors: errors?.tcas_report?.aircrafts[index] || {},
    touched: touched?.tcas_report?.aircrafts[index] || {},
  };

  return (
    <Row>
      <Cell span>
        <Box
          sx={{
            border: 1,
            borderRadius: 5,
            borderColor: "divider",
            mx: 1,
            mb: 2,
            mt: 0,
            p: 2,
            pt: 1,
          }}
        >
          <Row>
            <Cell span>
              <Typography variant="overline" color="textSecondary">{`Aéronef ${
                index + 1
              }`}</Typography>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <FormTextField
                label="Indicatif"
                id="callsign"
                onChange={(e) => handleChange(e, "callsign")}
                {...form_props}
                inputProps={{
                  style: { textTransform: "uppercase" },
                }}
              />
            </Cell>
            <Cell span>
              <FormTextField
                label="Code SSR"
                id="ssr"
                inputProps={{
                  inputMode: "numeric",
                }}
                pattern={SSR_PATTERN}
                {...form_props}
                onChange={(e) => handleChange(e, "ssr")}
              />
            </Cell>
            <Cell span={1} alignItems="flex-end">
              <IconButton color="error" onClick={handleDelete}>
                <Delete />
              </IconButton>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <FormSelectField
                label="Phase de vol"
                id="flight_phase"
                choices={FLIGHT_PHASES.map(({ value }) => value)}
                {...form_props}
                onChange={(e) => handleChange(e, "flight_phase")}
                getOptionLabel={(option) =>
                  FLIGHT_PHASES.find(({ value }) => value === option)?.label ||
                  ""
                }
              />
            </Cell>
            <Cell span>
              <FormTextField
                fullWidth
                label="FL assigné"
                id="assigned_fl"
                inputProps={{
                  inputMode: "numeric",
                }}
                pattern={FL_PATTERN}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">FL</InputAdornment>
                  ),
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "assigned_fl")}
              />
            </Cell>
            <Cell span>
              <FormTextField
                fullWidth
                label="FL réel"
                id="real_fl"
                inputProps={{
                  inputMode: "numeric",
                }}
                pattern={FL_PATTERN}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">FL</InputAdornment>
                  ),
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "real_fl")}
              />
            </Cell>
          </Row>
          <Row>
            <Cell alignItems="flex-end" span>
              <FormRadioField
                id="is_origin"
                label="Origine du signalement"
                choices={YES_NO_CHOICES}
                boolean
                {...form_props}
                onChange={(e) => handleChange(e, "is_origin")}
              />
            </Cell>
            <Cell alignItems="flex-end" span>
              <FormRadioField
                label="Type d'avis"
                id="advisory_type"
                choices={TCAS_TYPES}
                {...form_props}
                onChange={(e) => handleChange(e, "advisory_type")}
              />
            </Cell>
            <Cell alignItems="flex-end" span>
              <FormRadioField
                label="Contact radio"
                id="contact_radio"
                choices={YES_NO_CHOICES}
                boolean
                onChange={(e) => handleChange(e, "contact_radio")}
                {...form_props}
              />
            </Cell>
            <Cell alignItems="flex-end" span>
              <FormRadioField
                id="is_vfr"
                label="VFR"
                choices={YES_NO_CHOICES}
                boolean
                onChange={(e) => handleChange(e, "is_vfr")}
                {...form_props}
              />
            </Cell>
            <Cell alignItems="flex-end" span>
              <FormRadioField
                id="is_mil"
                label="Militaire"
                choices={YES_NO_CHOICES}
                boolean
                onChange={(e) => handleChange(e, "is_mil")}
                {...form_props}
              />
            </Cell>
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
