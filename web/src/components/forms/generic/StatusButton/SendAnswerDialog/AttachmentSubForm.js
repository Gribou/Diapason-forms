import React from "react";
import { Typography, Stack } from "@mui/material";

import { useSubForm } from "features/ui";
import { FormCheckboxField } from "components/forms/fields";
import {
  formatBytes,
  ellipsize,
} from "components/forms/generic/detail/AttachmentPart/RowDisplay";

export default function AttachmentSubForm({
  values,
  error,
  touched,
  onChange,
  index,
}) {
  const { handleChange } = useSubForm({
    index,
    root_key: "attachments",
    values,
    onChange,
  });

  const form_props = {
    values: values?.attachments?.[index],
    errors: error?.attachments?.[index],
    touched: touched?.attachments?.[index],
  };

  const { file_url, name, author, size } = values?.attachments?.[index] || {};
  const filename = file_url?.split("/").reverse()[0] || name;
  const pretty_size = Number.isInteger(size) ? formatBytes(size) : size;

  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="stretch"
      spacing={2}
      sx={{ py: 1 }}
    >
      <Typography sx={{ flexGrow: 1 }}>
        {ellipsize(filename) || "<vide>"}
      </Typography>
      {author && (
        <Typography color="textSecondary" variant="caption" noWrap>
          {`par ${author}`}
        </Typography>
      )}
      <Typography color="textSecondary" variant="caption" noWrap>
        {pretty_size}
      </Typography>
      <FormCheckboxField
        id="include"
        label="Inclure"
        {...form_props}
        onChange={(event) => handleChange(event, "include")}
        sx={{ width: "auto" }}
      />
    </Stack>
  );
}
