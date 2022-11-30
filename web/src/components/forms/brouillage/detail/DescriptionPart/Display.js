import React from "react";
import {
  Part,
  Row,
  LabelCell,
  ValueCell,
  BooleanCell,
  Cell,
} from "components/misc/PageElements";
import CopyToClipboardButton from "components/misc/CopyToClipboardButton";

export default function Display({ data, ...props }) {
  return (
    <Part title="Description de l'évènement" defaultExpanded {...props}>
      <Row>
        <LabelCell label="Type de brouillage" />
        <ValueCell
          value={data?.interferences?.map(({ name }) => name)?.join(", ")}
        />
      </Row>
      <Row>
        <BooleanCell
          label="Fréquence inutilisable"
          value={data?.freq_unusable}
          span
        />
        <BooleanCell
          label="Impact sur le trafic"
          value={data?.traffic_impact}
          span
        />
        <BooleanCell
          label="Fréquence supplétive utilisée"
          value={data?.supp_freq}
          span
        />
      </Row>
      <Row sx={{ pt: 2 }}>
        <LabelCell
          span={false}
          label="Commentaire"
          justifyContent="center"
          direction="row"
        />
        <Cell span>
          <CopyToClipboardButton content={data?.description} />
        </Cell>
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
