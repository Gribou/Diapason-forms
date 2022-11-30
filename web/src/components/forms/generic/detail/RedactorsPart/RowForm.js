import React from "react";
import { IconButton, Tooltip } from "@mui/material";
import { Delete, EmailOutline, EmailAlertOutline } from "mdi-material-ui";

import { Row, Cell } from "components/misc/PageElements";
import { useSubForm } from "features/ui";
import { FormTextField, FormSelectField } from "components/forms/fields";
import useEmailDialog from "./EmailDialog";

export default function RedactorSubForm({
  index,
  item,
  values,
  teams,
  roles,
  onChange,
  errors,
  touched,
  showRole,
  ...props
}) {
  const { handleChange, handleDelete } = useSubForm({
    index,
    root_key: "redactors",
    values,
    onChange,
  });

  const form_props = {
    values: item,
    errors: errors?.redactors ? errors?.redactors[index] : {},
    touched: touched?.redactors ? touched?.redactors[index] || {} : {},
  };

  const emailDialog = useEmailDialog({
    onChange: (e) => handleChange(e, "email"),
    ...form_props,
  });

  return (
    <Row {...props}>
      <Cell span={4} alignItems="flex-start">
        <FormTextField
          label="Prénom NOM"
          id="fullname"
          onChange={(event) => handleChange(event, "fullname")}
          {...form_props}
          inputProps={{ style: { textTransform: "capitalize" } }}
        />
      </Cell>
      <Cell span={3} alignItems="flex-start">
        <FormSelectField
          label="Equipe"
          id="team"
          choices={teams?.map(({ label }) => label)}
          {...form_props}
          value={
            (typeof item?.team === "string" || item?.team instanceof String
              ? item?.team
              : item?.team?.label) || ""
          }
          onChange={(event) => handleChange(event, "team")}
        />
      </Cell>
      {showRole && (
        <Cell span={3} alignItems="flex-start">
          <FormSelectField
            label="Rôle"
            choices={roles}
            id="role"
            {...form_props}
            onChange={(e) => handleChange(e, "role")}
          />
        </Cell>
      )}
      <Cell alignItems="flex-start">
        <Tooltip
          title={`Notifications par e-mail${
            item?.email ? ` (${item?.email}@aviation-civile.gouv.fr)` : ""
          }`}
        >
          <IconButton
            onClick={emailDialog.open}
            color={item?.email ? "primary" : undefined}
            sx={{ mt: 1 }}
          >
            {form_props?.errors?.email ? (
              <EmailAlertOutline />
            ) : (
              <EmailOutline />
            )}
          </IconButton>
        </Tooltip>
      </Cell>
      <Cell span justifyContent="flex-end" alignItems="flex-start">
        <IconButton color="error" onClick={handleDelete} sx={{ mt: 1 }}>
          <Delete />
        </IconButton>
      </Cell>
      {emailDialog.display}
    </Row>
  );
}
