import React from "react";
import { Stack } from "@mui/material";
import { useSearchParams } from "features/router";
import { useFormConfig } from "features/config/hooks";
import SortButton from "./SortButton";
import FilterButton from "./Filters";
import SearchFilter from "./SearchFilter";
import GlobalMenuButton from "./GlobalMenuButton";
import { getDefaultTab } from "../config";
import ActiveFiltersDisplay from "./ActiveFiltersDisplay";

export default function Filters({ data }) {
  const [params] = useSearchParams();
  const form_key = params?.form_key || getDefaultTab(data);
  const current_meta = data?.forms?.[form_key];
  const { safetycube_enabled } = useFormConfig(form_key);

  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="flex-end"
      spacing={1}
      sx={{
        mt: 1,
        flex: "1 1 0%",
        minWidth: 0,
        flexWrap: "wrap",
        rowGap: "4px",
      }}
    >
      <SortButton />
      <FilterButton meta={current_meta} />
      <ActiveFiltersDisplay />
      <SearchFilter />
      {safetycube_enabled && (
        <GlobalMenuButton form_key={form_key || getDefaultTab(data)} />
      )}
    </Stack>
  );
}
