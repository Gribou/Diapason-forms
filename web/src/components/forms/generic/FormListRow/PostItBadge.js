import React from "react";
import { Badge } from "@mui/material";
import { NoteOutline } from "mdi-material-ui";

export default function PostItBadge({ count, sx }) {
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
      <NoteOutline color="action" />
    </Badge>
  );
}
