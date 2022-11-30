import React from "react";
import { Typography } from "@mui/material";
import { Part, Row, Cell } from "components/misc/PageElements";

export default function Display({
  items,
  item_name,
  item_name_plural,
  empty_text,
  rowProps,
  RowComponent,
  ...props
}) {
  return (
    <Part
      title={`${items?.length || 0} ${
        items?.length > 1 ? item_name_plural || `${item_name}s` : item_name
      }`}
      defaultExpanded
      {...props}
    >
      {items?.map((item, i) => (
        <RowComponent key={i} index={i} item={item} {...rowProps} />
      ))}
      {(!items || items.length === 0) && (
        <Row>
          <Cell span>
            <Typography color="textSecondary" variant="subtitle1">
              {empty_text}
            </Typography>
          </Cell>
        </Row>
      )}
    </Part>
  );
}
