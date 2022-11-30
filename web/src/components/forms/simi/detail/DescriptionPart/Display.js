import React from "react";
import {
  Part,
  Row,
  LabelCell,
  ValueCell,
  Cell,
  BooleanCell,
} from "components/misc/PageElements";
import CopyToClipboardButton from "components/misc/CopyToClipboardButton";

export default function Display({ data, ...props }) {
  return (
    <Part title="Description de l'évènement" defaultExpanded {...props}>
      <Row sx={{ pt: 2 }}>
        <LabelCell
          span={false}
          label="Description"
          direction="column"
          justifyContent="center"
        />
        <Cell span>
          <CopyToClipboardButton content={data?.description} />
        </Cell>
        <BooleanCell label="Avec incident" value={data?.with_incident} />
      </Row>
      <Row sx={{ pt: 1 }}>
        <ValueCell
          span
          value={data?.description}
          sx={{ whiteSpace: "pre-wrap" }}
        />
      </Row>
    </Part>
  );
}
