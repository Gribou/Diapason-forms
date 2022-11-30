import React from "react";
import {
  Part,
  Row,
  LabelCell,
  ValueCell,
  Cell,
} from "components/misc/PageElements";
import CopyToClipboardButton from "components/misc/CopyToClipboardButton";
import { PhotoDisplay } from "components/forms/fields";

export default function Display({ data, ...props }) {
  return (
    <Part title="Description de l'évènement" defaultExpanded {...props}>
      <Row>
        <LabelCell label="Type(s) d'évènement" />
        <ValueCell
          value={data?.event_types?.map(({ name }) => name)?.join(", ")}
        />
      </Row>
      <Row>
        <LabelCell label="Evènement technique" />
        <ValueCell
          value={data?.tech_event
            ?.filter((ev) => ev)
            .map(({ name }) => name)
            ?.join(", ")}
        />
      </Row>
      <Row>
        <LabelCell label="Actions entreprises" />
        <ValueCell
          value={(data?.tech_actions_done || [])
            ?.filter((a) => a)
            ?.map(({ name }) => name)
            ?.join(", ")}
        />
      </Row>
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
        {data?.drawing_url && (
          <Cell justifyContent="space-between">
            <PhotoDisplay title="Schéma descriptive" url={data?.drawing_url} />
          </Cell>
        )}
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
