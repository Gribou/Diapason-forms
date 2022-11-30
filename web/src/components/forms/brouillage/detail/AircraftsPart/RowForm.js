import React from "react";
import { Box, Typography, IconButton, InputAdornment } from "@mui/material";
import { Delete } from "mdi-material-ui";

import { Row, Cell } from "components/misc/PageElements";
import {
  FormTextField,
  PhotoField,
  FormRadioField,
} from "components/forms/fields";
import { useFeatures } from "features/config/hooks";
import { useSubForm } from "features/ui";
import { FL_PATTERN, FLOAT_PATTERN, INTEGER_PATTERN } from "constants/config";
import { AIR_OR_GROUND } from "constants/brouillage";

export default function AircraftSubForm({
  index,
  item,
  values,
  onChange,
  errors,
  touched,
  ...props
}) {
  const { stripless } = useFeatures();
  const { handleChange, handleDelete } = useSubForm({
    index,
    root_key: "aircrafts",
    values,
    onChange,
  });

  const form_props = {
    values: item,
    errors: errors?.aircrafts?.[index] || {},
    touched: touched?.aircrafts?.[index] || {},
  };

  const handleStripDelete = () => {
    const new_aircrafts = (values?.aircrafts || []).map((r, i) =>
      i === index ? { ...r, strip_url: undefined, strip: undefined } : r
    );
    onChange({
      target: { name: "aircrafts", value: new_aircrafts },
    });
  };

  return (
    <Row {...props}>
      <Cell span>
        <Box
          border={1}
          borderRadius={5}
          borderColor="divider"
          m={1}
          mb={2}
          mt={0}
          p={2}
          pt={1}
        >
          <Row alignItems="center">
            <Cell span={3}>
              <FormTextField
                label="Indicatif"
                id="callsign"
                onChange={(event) => handleChange(event, "callsign")}
                {...form_props}
                inputProps={{ style: { textTransform: "uppercase" } }}
              />
            </Cell>
            <Cell>
              <PhotoField
                {...form_props}
                id="strip"
                url_id="strip_url"
                label={stripless ? "Photo" : "Strip"}
                helperText={
                  stripless
                    ? "Prendre une photo de l'aéronef"
                    : "Prendre une photo du/des strips"
                }
                onChange={(e) => handleChange(e, "strip")}
                onDelete={handleStripDelete}
                onSaveMessage={`Photo ${stripless ? "" : "du strip "}${
                  item.callsign?.toUpperCase() || ""
                } enregistrée`}
                onDeleteMessage={`Photo ${stripless ? "" : "du strip "}${
                  item.callsign?.toUpperCase() || ""
                } supprimée`}
              />
            </Cell>
            <Cell span />
            <Cell>
              <Typography variant="overline" color="textSecondary">{`Aéronef ${
                index + 1
              }`}</Typography>
            </Cell>
            <Cell justifyContent="flex-end">
              <IconButton color="error" onClick={handleDelete}>
                <Delete />
              </IconButton>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <FormTextField
                label="Balise"
                id="waypoint"
                inputProps={{
                  style: { textTransform: "uppercase" },
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "waypoint")}
              />
            </Cell>
            <Cell span={3}>
              <FormTextField
                label="Distance"
                id="distance"
                inputProps={{ inputMode: "numeric" }}
                pattern={FLOAT_PATTERN}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">NM</InputAdornment>
                  ),
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "distance")}
              />
            </Cell>
            <Cell span={3}>
              <FormTextField
                label="Relèvement"
                id="bearing"
                inputProps={{ inputMode: "numeric" }}
                patter={INTEGER_PATTERN}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">°</InputAdornment>
                  ),
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "bearing")}
              />
            </Cell>
          </Row>
          <Row>
            <Cell span={3}>
              <FormTextField
                label="FL"
                id="fl"
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
                onChange={(e) => handleChange(e, "fl")}
              />
            </Cell>
            <Cell span />
            <Cell span={6}>
              <FormRadioField
                id="plaintiff"
                choices={AIR_OR_GROUND}
                label="Reçu par"
                radioSx={{ flex: "1 1 0%", mr: 0 }}
                {...form_props}
                onChange={(e) => handleChange(e, "plaintiff")}
              />
            </Cell>
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
