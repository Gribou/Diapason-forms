import React from "react";
import { Box, CircularProgress } from "@mui/material";

export default function LoadingGraph(props) {
  return (
    <Box
      sx={{
        flexGrow: 1,
        minHeight: "300px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        pb: 2,
      }}
      {...props}
    >
      <CircularProgress />
    </Box>
  );
}
