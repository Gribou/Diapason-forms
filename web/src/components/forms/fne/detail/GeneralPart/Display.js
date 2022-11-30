import React from "react";
import moment from "moment-timezone";

import { DATETIME_DISPLAY_FORMAT } from "constants/config";
import {
  Part,
  Row,
  LabelCell,
  ValueCell,
  BooleanCell,
} from "components/misc/PageElements";

export default function Display({ data, ...props }) {
  return (
    <Part title="Informations générales" defaultExpanded {...props}>
      <Row>
        <LabelCell label="Date et heure de l'évènement" />
        <ValueCell
          value={
            data.event_date &&
            moment(data?.event_date).format(DATETIME_DISPLAY_FORMAT + " TU")
          }
        />
      </Row>
      <Row>
        <BooleanCell
          singleCell={false}
          label="Instruction sur Position"
          noColon
          value={data?.isp}
        />
      </Row>
      {(data?.secteur || data?.position || data?.regroupement) && (
        <Row>
          <LabelCell label="Secteur/Position/Regroupement" />
          <ValueCell
            value={`${data.secteur || "?"}/${data.position || "?"}/${
              data.regroupement || "?"
            }`}
          />
        </Row>
      )}
      {data?.lieu && (
        <Row>
          <LabelCell label="Lieu de l'évènement" />
          <ValueCell value={data.lieu} />
        </Row>
      )}
    </Part>
  );
}
