import React from "react";
import { Row, LabelCell, ValueCell } from "components/misc/PageElements";

export default function RedactorRow({ item, showRole, ...props }) {
  const { role, team, fullname, email } = item;
  return (
    <Row {...props}>
      {showRole && <LabelCell label={role} />}
      <ValueCell
        value={`${fullname} (${team.label || "équipe ?"}${
          email ? ` - ${email}` : ""
        })`}
      />
    </Row>
  );
}
