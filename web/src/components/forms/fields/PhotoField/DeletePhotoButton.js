import React from "react";
import { useDispatch } from "react-redux";
import { Tooltip, IconButton } from "@mui/material";
import { Close } from "mdi-material-ui";

import { displayMessage } from "features/messages";

export default function DeletePhotoButton({
  id,
  id_url,
  file,
  url,
  onDeleteMessage = "Photo supprimée",
  onChange,
  ...props
}) {
  const dispatch = useDispatch();

  const handlePhotoDelete = () => {
    onChange([
      {
        target: { name: id, value: undefined },
      },
      {
        target: { name: id_url, value: undefined },
      },
    ]);
    dispatch(displayMessage(onDeleteMessage));
  };

  return (
    <Tooltip title="Supprimer la photo">
      <span>
        <IconButton
          size="small"
          color="error"
          disabled={!(file || url)}
          onClick={handlePhotoDelete}
          {...props}
        >
          <Close />
        </IconButton>
      </span>
    </Tooltip>
  );
}
