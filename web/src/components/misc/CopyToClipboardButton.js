import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { ContentCopy } from "mdi-material-ui";

export default function CopyToClipboardButton({ content }) {
  return (
    <Tooltip title="Copier dans le presse-papier">
      <span>
        <IconButton
          size="small"
          disabled={!content}
          onClick={() => navigator.clipboard.writeText(content)}
        >
          <ContentCopy />
        </IconButton>
      </span>
    </Tooltip>
  );
}
