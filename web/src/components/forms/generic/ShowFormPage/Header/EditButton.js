import React, { useState } from "react";
import { Tooltip, IconButton } from "@mui/material";
import { Pencil } from "mdi-material-ui";

export default function useEditButton() {
  const [editMode, setEditMode] = useState(false);

  const display = !editMode && (
    <Tooltip title="Editer">
      <IconButton
        color="primary"
        size="small"
        onClick={() => setEditMode(true)}
      >
        <Pencil />
      </IconButton>
    </Tooltip>
  );

  const reset = () => {
    if (editMode) setEditMode(false);
  };

  return { value: editMode, display, reset };
}
