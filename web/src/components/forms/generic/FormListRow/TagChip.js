import React from "react";
import { TagOutline } from "mdi-material-ui";
import formMappings from "features/forms/mappings";
import NormalChip from "./NormalChip";

export default function TagChip({ uuid, keyword, keywords, form_key }) {
  const [set_keywords, { isLoading }] =
    formMappings[form_key]?.set_keywords() || [];

  const onDelete = () => {
    set_keywords({
      uuid,
      keywords: keywords?.filter((word) => word !== keyword && word),
    });
  };

  return (
    <NormalChip
      label={keyword}
      IconComponent={TagOutline}
      loading={isLoading}
      onDelete={onDelete}
      variant="outlined"
    />
  );
}
