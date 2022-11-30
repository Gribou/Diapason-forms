import React from "react";
import { Avatar } from "@mui/material";

export default function RowAvatar({ zones, sx = [] }) {
  const category_color =
    zones?.length === 1
      ? zones[0]?.color
      : zones?.length
      ? "text.secondary"
      : undefined;

  return (
    <Avatar
      sx={[{ bgcolor: category_color }, ...(Array.isArray(sx) ? sx : [sx])]}
    >
      {zones?.map(({ name }) => name)?.join("") || "?"}
    </Avatar>
  );
}
