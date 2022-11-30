import React from "react";
import moment from "moment-timezone";
import { Part, Row, LabelCell, ValueCell } from "components/misc/PageElements";
import { DATETIME_DISPLAY_FORMAT } from "constants/config";

export default function Display({ data, ...props }) {
  return (
    <Part title="Informations générales" defaultExpanded {...props}>
      <Row>
        <LabelCell label="Date et heure de l'évènement" />
        <ValueCell
          value={
            data?.event_date &&
            moment(data?.event_date).format(DATETIME_DISPLAY_FORMAT + " TU")
          }
        />
      </Row>
      <Row>
        <LabelCell label="Fréquence" />
        <ValueCell value={data?.frequency} />
      </Row>
      <Row>
        <LabelCell label="Position de contrôle" />
        <ValueCell value={data?.cwp} />
      </Row>
    </Part>
  );
}
