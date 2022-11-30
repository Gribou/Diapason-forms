import React from "react";
import { useMe } from "features/auth/hooks";
import { SIMI_FORM_KEY } from "features/forms/mappings";
import { GeneralPart, DescriptionPart, AircraftsPart, SubPart } from "./detail";
import { RedactorsPart, PostItPart } from "components/forms/generic/detail";

export default function SimiDisplay({ data, anonymous, ...props }) {
  const { is_investigator } = useMe();

  return (
    <div {...props}>
      {is_investigator && <SubPart data={data} />}
      <GeneralPart data={data} defaultExpanded />
      {!!data?.redactors?.length && !anonymous && (
        <RedactorsPart data={data} defaultExpanded />
      )}
      {!!data?.aircrafts?.length && <AircraftsPart data={data} />}
      <DescriptionPart data={data} defaultExpanded />
      {is_investigator && <PostItPart data={data} form_key={SIMI_FORM_KEY} />}
    </div>
  );
}
