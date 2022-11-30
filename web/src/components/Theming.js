import React from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import {
  cyan,
  blue,
  purple,
  deepOrange,
  yellow,
  pink,
  teal,
  green,
} from "@mui/material/colors";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";

const completeColor = (color) => ({
  ...color,
  main: color[500],
  light: color[300],
  dark: color[700],
});

const efne_theme = createTheme({
  palette: {
    primary: {
      ...cyan,
      contrastText: "#fff",
    },
    secondary: green,
    charts: [
      completeColor(blue),
      completeColor(deepOrange),
      completeColor(yellow),
      completeColor(pink),
      completeColor(teal),
      completeColor(purple),
    ],
    background: { paper: "#fff", default: "#fafafa" },
  },
});

const Theming = ({ children }) => (
  <ThemeProvider theme={efne_theme}>{children}</ThemeProvider>
);

export const getChartColor = (theme, index = 0, offset = 0) => {
  const palette_size = theme.palette.charts.length;
  return theme.palette.charts[(index + offset) % palette_size];
};

export default Theming;
