import React, { useState } from "react";
import { Tooltip, IconButton } from "@mui/material";
import { Eye, EyeOff } from "mdi-material-ui";

export default function useAnonymousButton() {
  const [anonymous, setAnonymous] = useState(false);

  const display = (
    <Tooltip title={anonymous ? "Dés-anonymiser" : "Anonymiser"}>
      <IconButton
        color="primary"
        size="small"
        onClick={() => setAnonymous(!anonymous)}
      >
        {anonymous ? <EyeOff /> : <Eye />}
      </IconButton>
    </Tooltip>
  );

  return { value: anonymous, display };
}
