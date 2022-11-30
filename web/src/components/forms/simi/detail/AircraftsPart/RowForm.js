import React from "react";
import { IconButton, Typography, Box, InputAdornment } from "@mui/material";
import { Delete } from "mdi-material-ui";

import { FL_PATTERN, SSR_PATTERN } from "constants/config";
import { useFeatures } from "features/config/hooks";
import { Row, Cell } from "components/misc/PageElements";
import { useSubForm } from "features/ui";
import { FormTextField, PhotoField } from "components/forms/fields";

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
    errors: errors?.aircrafts ? errors?.aircrafts[index] : {},
    touched: touched?.aircrafts ? touched?.aircrafts[index] : {},
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
            <Cell span>
              <FormTextField
                label="Type d'aéronef"
                id="type"
                inputProps={{ style: { textTransform: "uppercase" } }}
                {...form_props}
                onChange={(e) => handleChange(e, "type")}
              />
            </Cell>
            <Cell span>
              <FormTextField
                label="Provenance"
                id="provenance"
                inputProps={{
                  style: { textTransform: "uppercase" },
                  maxLength: 4,
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "provenance")}
              />
            </Cell>
            <Cell span>
              <FormTextField
                label="Destination"
                id="destination"
                inputProps={{
                  style: { textTransform: "uppercase" },
                  maxLength: 4,
                }}
                {...form_props}
                onChange={(e) => handleChange(e, "destination")}
              />
            </Cell>
          </Row>
          <Row>
            <Cell span={3}>
              <FormTextField
                fullWidth
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
            <Cell span>
              <FormTextField
                fullWidth
                label="Position"
                id="position"
                {...form_props}
                onChange={(e) => handleChange(e, "position")}
              />
            </Cell>
          </Row>
        </Box>
      </Cell>
    </Row>
  );
}
