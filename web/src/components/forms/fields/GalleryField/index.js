import React, { Fragment } from "react";
import { Tooltip, IconButton } from "@mui/material";
import { ImageMultiple } from "mdi-material-ui";

import useGalleryDialog from "./GalleryDialog";

export default function GalleryPhotoButton({ onChange, id, ...props }) {
  const dialog = useGalleryDialog((value) =>
    onChange({ target: { value, name: id } })
  );
  return (
    <Fragment>
      <Tooltip title="Choisir une photo dans la photothèque">
        <span>
          <IconButton
            size="small"
            color="primary"
            onClick={dialog.open}
            {...props}
          >
            <ImageMultiple />
          </IconButton>
        </span>
      </Tooltip>
      {dialog.display}
    </Fragment>
  );
}
