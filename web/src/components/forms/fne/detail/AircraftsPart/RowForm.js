import React from "react";
import { IconButton } from "@mui/material";
import { Delete } from "mdi-material-ui";

import { Row, Cell } from "components/misc/PageElements";
import { useSubForm } from "features/ui";
import { useFeatures } from "features/config/hooks";
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
      <Cell span={4}>
        <FormTextField
          label="Indicatif"
          id="callsign"
          onChange={(event) => handleChange(event, "callsign")}
          {...form_props}
          inputProps={{ style: { textTransform: "uppercase" } }}
        />
      </Cell>

      <Cell span={6}>
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
      <Cell span justifyContent="flex-end">
        <IconButton color="error" onClick={handleDelete}>
          <Delete />
        </IconButton>
      </Cell>
    </Row>
  );
}
