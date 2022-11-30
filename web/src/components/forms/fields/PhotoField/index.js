import React from "react";
import { Tooltip, IconButton, Typography, Stack, Box } from "@mui/material";
import { Camera } from "mdi-material-ui";

import { useFeatures } from "features/config/hooks";
import { usePhotoImport } from "features/photo";
import GalleryPhotoButton from "../GalleryField";
import ShowPhotoButton from "./ShowPhotoButton";
import DeletePhotoButton from "./DeletePhotoButton";

export { default as PhotoDisplay } from "./PhotoDisplay";
export { default as ShowPhotoButton } from "./ShowPhotoButton";
export { default as DeletePhotoButton } from "./DeletePhotoButton";

function PhotoLabel({ label, hasErrors, file, url, ...props }) {
  const ellipsize = (str) => (str.length > 25 ? "..." + str.slice(-25) : str);

  return (
    <Box {...props}>
      <Typography
        variant="overline"
        sx={{ mr: 1, lineHeight: 1 }}
        color={hasErrors ? "error" : "textPrimary"}
      >
        {`${label} : `}
      </Typography>
      <Typography
        variant="overline"
        color={hasErrors ? "error" : "textSecondary"}
        sx={{
          flex: "1 1 0",
          overflow: "hidden",
          textOverflow: "ellipsis",
          lineHeight: 1,
        }}
        noWrap
      >
        {ellipsize(file ? "image importée" : url || "<vide>")}
      </Typography>
    </Box>
  );
}

function ImportPhotoButton({
  id,
  onChange,
  messageOnSave = "Photo enregistrée",
  ...props
}) {
  const handlePhotoImport = usePhotoImport(
    (file) =>
      onChange({
        target: {
          name: id,
          value: file,
        },
      }),
    messageOnSave
  );

  return (
    <Tooltip title="Prendre une photo">
      <span>
        <IconButton component="label" color="primary" size="small" {...props}>
          <Camera />
          <input
            hidden
            type="file"
            accept="image/*;capture=camera"
            id={id}
            onChange={handlePhotoImport}
          />
        </IconButton>
      </span>
    </Tooltip>
  );
}

export default function PhotoField({
  values,
  errors,
  id,
  url_id,
  label,
  onChange,
  onDelete,
  onSaveMessage,
  onDeleteMessage,
  helperText = "",
  sx = [],
  ...props
}) {
  const { gallery_url } = useFeatures();
  const showError = () => Boolean(errors?.[id]);

  return (
    <Stack
      direction="row"
      sx={[{ alignSelf: "center" }, ...(Array.isArray(sx) ? sx : [sx])]}
      {...props}
    >
      <Stack
        justifyContent="center"
        sx={{
          mr: 2,
          flexGrow: 1,
          whiteSpace: "nowrap",
          overflow: "ellipsize",
        }}
      >
        <PhotoLabel
          hasErrors={showError()}
          file={values?.[id]}
          url={values?.[url_id]}
          label={label}
        />
        <Typography
          variant="caption"
          color={showError() ? "error" : "textSecondary"}
        >
          {errors?.[id] || helperText}
        </Typography>
      </Stack>
      <Stack sx={{ whiteSpace: "nowrap" }} direction="row" alignItems="center">
        <ImportPhotoButton
          id={id}
          onChange={onChange}
          messageOnSave={onSaveMessage}
        />
        {gallery_url && <GalleryPhotoButton id={id} onChange={onChange} />}
        <ShowPhotoButton file={values?.[id]} url={values?.[url_id]} />
        <DeletePhotoButton
          id={id}
          id_url={url_id}
          file={values?.[id]}
          url={values?.[url_id]}
          onDeleteMessage={onDeleteMessage}
          onChange={onDelete || onChange}
        />
      </Stack>
    </Stack>
  );
}
