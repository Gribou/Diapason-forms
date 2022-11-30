import React from "react";

import { Part, Row, LabelCell, ValueCell } from "components/misc/PageElements";

export default function SubPart({ data }) {
  const { keywords } = data;

  return (
    <Part title="Enquête" defaultExpanded>
      <Row>
        <LabelCell label="Mots-clés" />
        <ValueCell value={keywords} />
      </Row>
    </Part>
  );
}
