import React, { Fragment } from "react";
import { useDispatch } from "react-redux";
import { IconButton, Tooltip, Typography, Stack, Box } from "@mui/material";
import { Draw } from "mdi-material-ui";

import useDrawingDialog from "./DrawingDialog";
import { ShowPhotoButton, DeletePhotoButton } from "../PhotoField";
import { displayMessage } from "features/messages";

function DrawButton({
  id,
  label,
  onChange,
  messageOnSave = "Schéma enregistré",
  ...props
}) {
  const dispatch = useDispatch();
  const handleChange = (new_image) => {
    onChange({ target: { name: id, value: new_image } });
    dispatch(displayMessage(messageOnSave));
  };
  const dialog = useDrawingDialog(label, handleChange);

  return (
    <Fragment>
      <Tooltip title="Faire un schéma">
        <IconButton
          color="primary"
          size="small"
          onClick={dialog.open}
          {...props}
        >
          <Draw />
        </IconButton>
      </Tooltip>
      {dialog.display}
    </Fragment>
  );
}

export default function DrawingField({
  values,
  errors,
  id,
  label,
  onChange,
  helperText = "",
}) {
  const showError = () => Boolean(errors?.[id]);

  return (
    <Stack direction="row">
      <Box
        sx={{ mr: 2, flexGrow: 1, whiteSpace: "nowrap", overflow: "ellipsize" }}
      >
        <Typography
          variant="overline"
          color={showError() ? "error" : "textPrimary"}
        >
          {`${label} : `}
        </Typography>
        <Typography
          variant="caption"
          color={showError() ? "error" : "textSecondary"}
        >
          {errors?.[id] || helperText}
        </Typography>
      </Box>
      <Stack direction="row" sx={{ whiteSpace: "nowrap" }}>
        <DrawButton id={id} onChange={onChange} label={label} />
        <ShowPhotoButton url={values?.[id]} dialogProps={{ maxWidth: "xl" }} />
        <DeletePhotoButton id={id} url={values?.[id]} onChange={onChange} />
      </Stack>
    </Stack>
  );
}
