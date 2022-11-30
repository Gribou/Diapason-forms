import React from "react";
import { Grid } from "@mui/material";

export default function ButtonBox({ children }) {
  return (
    <Grid
      container
      direction="row"
      sx={{ alignItems: "center", justifyContent: "center" }}
      spacing={1}
    >
      {(Array.isArray(children) ? children : [children])?.map((button, i) => (
        <Grid item key={i}>
          {button}
        </Grid>
      ))}
    </Grid>
  );
}
