import React from "react";
import { Badge } from "@mui/material";
import { Paperclip } from "mdi-material-ui";

export default function AttachmentBadge({ count, sx }) {
  return (
    <Badge
      badgeContent={count}
      color="secondary"
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "right",
      }}
      sx={sx}
    >
      <Paperclip color="action" />
    </Badge>
  );
}
