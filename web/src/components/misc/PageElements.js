import React, { Fragment } from "react";
import {
  Grid,
  Typography,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import { ChevronDown } from "mdi-material-ui";

export const Row = ({ children, spacing = 2, ...props }) => (
  <Grid xs={12} container item spacing={spacing} {...props}>
    {children}
  </Grid>
);

export const Cell = ({
  children,
  span,
  justifyContent = "flex-start",
  alignItems = "center",
  direction = "row",
  sx = [],
  ...props
}) => (
  <Grid
    item
    xs={span}
    sx={[
      {
        display: "flex",
        flexDirection: direction,
        alignItems: alignItems,
        justifyContent: justifyContent,
      },
      ...(Array.isArray(sx) ? sx : [sx]),
    ]}
    {...props}
  >
    {children}
  </Grid>
);

export function LabelCell({ label, noColon, span = 4, ...props }) {
  return (
    <Cell span={span} {...props}>
      <Typography component="span" variant="subtitle2">{`${label}${
        noColon ? "" : " : "
      }`}</Typography>
    </Cell>
  );
}

export function ValueCell({ value, anonymous, span = true, ...props }) {
  return (
    <Cell span={span} {...props}>
      {anonymous ? (
        <Typography
          component="span"
          variant="body2"
          align="justify"
          sx={{ bgcolor: "common.black" }}
        >
          {Array(value.length || 25).join("_")}
        </Typography>
      ) : (
        <Typography component="span" variant="body2" align="justify">
          {value || "..."}
        </Typography>
      )}
    </Cell>
  );
}

export function BooleanCell({
  label,
  value,
  singleCell = true,
  noColon,
  yesLabel = "Oui",
  noLabel = "Non",
  span,
  ...props
}) {
  const value_display =
    value === undefined ? "..." : value ? yesLabel : noLabel;

  return singleCell ? (
    <Cell {...props} span={span}>
      <Typography component="span" variant="subtitle2" sx={{ mr: 1 }}>
        {`${label}${noColon ? "" : " : "}`}
      </Typography>
      <Typography component="span" variant="body2">
        {value_display}
      </Typography>
    </Cell>
  ) : (
    <Fragment>
      <LabelCell label={label} span={span} noColon={noColon} />
      <ValueCell value={value_display} />
    </Fragment>
  );
}

export const Part = ({
  children,
  title,
  addOn,
  titleProps,
  hideExpandIcon = false,
  ...props
}) => (
  <Accordion {...props}>
    {(title || !hideExpandIcon) && (
      <AccordionSummary expandIcon={!hideExpandIcon && <ChevronDown />}>
        <Grid container>
          <Grid xs item>
            <Typography component="h2" variant="h6" {...titleProps}>
              {title}
            </Typography>
          </Grid>
          {addOn && <Grid item>{addOn}</Grid>}
        </Grid>
      </AccordionSummary>
    )}
    <AccordionDetails>
      <Grid container>{children}</Grid>
    </AccordionDetails>
  </Accordion>
);

export const DividerRow = ({ sx = [], ...props }) => (
  <Row>
    <Cell span>
      <Divider
        variant="middle"
        sx={[{ mt: 2, mb: 2 }, ...(Array.isArray(sx) ? sx : [sx])]}
        {...props}
      />
    </Cell>
  </Row>
);
