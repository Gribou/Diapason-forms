import React from "react";

import { useMe } from "features/auth/hooks";

import {
  GeneralPart,
  DescriptionPart,
  CdsPart,
  TcasPart,
  AircraftsPart,
  SubPart,
} from "./detail";
import {
  RedactorsPart,
  PostItPart,
  AttachmentPart,
} from "components/forms/generic/detail";
import { FNE_FORM_KEY } from "features/forms/mappings";

export default function FneDisplay({ data, anonymous, ...props }) {
  const { is_investigator } = useMe();

  return (
    <div {...props}>
      {is_investigator && <SubPart data={data} />}
      <GeneralPart data={data} defaultExpanded />
      {!!data?.redactors?.length && !anonymous && (
        <RedactorsPart data={data} showRole defaultExpanded />
      )}
      {!!data?.aircrafts?.length && <AircraftsPart data={data} />}
      <DescriptionPart data={data} defaultExpanded />
      {data?.tcas_report && <TcasPart data={data} />}
      {data?.cds_report && <CdsPart data={data} />}
      <AttachmentPart data={data} form_key={FNE_FORM_KEY} defaultExpanded />
      {is_investigator && <PostItPart data={data} form_key={FNE_FORM_KEY} />}
    </div>
  );
}
