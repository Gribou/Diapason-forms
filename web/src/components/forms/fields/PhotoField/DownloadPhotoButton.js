import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { Download } from "mdi-material-ui";

export default function DownloadPhotoButton({ url, ...props }) {
  return (
    <Tooltip title="Télécharger l'image">
      <span>
        <IconButton
          size="small"
          disabled={!url}
          component="a"
          href={url || ""}
          target="_blank"
          rel="noreferrer"
          color="primary"
          download={`${url?.split(".")[-1] || ""}`}
          {...props}
        >
          <Download />
        </IconButton>
      </span>
    </Tooltip>
  );
}
