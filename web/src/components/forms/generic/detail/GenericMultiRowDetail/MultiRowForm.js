import React from "react";
import { Button } from "@mui/material";
import { Plus } from "mdi-material-ui";

import { Part } from "components/misc/PageElements";
import { addRow } from "features/ui";

export default function Form({
  formProps,
  item_name,
  item_name_plural,
  item_key,
  SubFormComponent,
  rowProps,
  ...props
}) {
  const { values, onChange } = formProps;

  return (
    <Part
      title={item_name_plural || `${item_name}s`}
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
            addRow(item_key, values, onChange);
          }}
          sx={{ mr: 1 }}
        >
          {`Ajouter ${item_name}`}
        </Button>
      }
      {...props}
    >
      {values?.[item_key]?.map((r, i) => (
        <SubFormComponent
          key={i}
          index={i}
          item={r}
          {...formProps}
          {...rowProps}
        />
      ))}
    </Part>
  );
}
