import React, { Fragment } from "react";
import {
  Part,
  Row,
  Cell,
  LabelCell,
  BooleanCell,
  ValueCell,
  DividerRow,
} from "components/misc/PageElements";
import CopyToClipboardButton from "components/misc/CopyToClipboardButton";

export default function Display({ data, ...props }) {
  const { cds_report: cdsReport } = data;
  return (
    <Part title="Chef de Salle" defaultExpanded {...props}>
      <Row>
        <BooleanCell
          span
          label="Notification RPO"
          value={cdsReport?.notif_rpo}
        />
        <BooleanCell
          span
          label="Constat Préalable d'Infraction"
          value={cdsReport?.cpi}
        />
        <BooleanCell
          span
          label="REX Chef de Salle"
          value={cdsReport?.rex_cds}
        />
      </Row>
      {cdsReport?.com_cds && (
        <Fragment>
          <DividerRow />
          <Row style={{ paddingTop: "8px" }}>
            <LabelCell
              span={false}
              label="Commentaire"
              direction="column"
              justifyContent="center"
            />
            <Cell>
              <CopyToClipboardButton content={cdsReport?.com_cds} />
            </Cell>
          </Row>
          <Row sx={{ pt: 1 }}>
            <ValueCell
              span
              value={cdsReport?.com_cds}
              sx={{ whiteSpace: "pre-wrap" }}
            />
          </Row>
        </Fragment>
      )}
    </Part>
  );
}
