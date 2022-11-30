import React, { Fragment } from "react";
import { Tooltip, IconButton } from "@mui/material";
import { Eye } from "mdi-material-ui";

import usePhotoPreviewDialog from "./PhotoPreviewDialog";

export default function ShowPhotoButton({ file, url, dialogProps, ...props }) {
  const preview = usePhotoPreviewDialog(
    file ? URL.createObjectURL(file) : url,
    dialogProps
  );

  return (
    <Fragment>
      <Tooltip title="Voir un aperçu">
        <span>
          <IconButton
            size="small"
            color="primary"
            disabled={!(file || url)}
            onClick={preview.open}
            {...props}
          >
            <Eye />
          </IconButton>
        </span>
      </Tooltip>
      {preview.display}
    </Fragment>
  );
}
