import React from "react";
import { Stack, Chip } from "@mui/material";
import {
  Web,
  Shape,
  TimerSandEmpty,
  AccountMultiple,
  TagOutline,
} from "mdi-material-ui";
import SafetyCubeIcon from "components/logos/SafetyCubeIcon";
import { useSearchParams } from "features/router";

function FilterChip({ make_label = (v) => v, icon, param_key, ...props }) {
  const [params, push] = useSearchParams();
  return params?.[param_key] ? (
    <Chip
      size="small"
      label={make_label(params?.[param_key])?.replaceAll(",", " + ")}
      icon={icon}
      onDelete={() =>
        push({
          ...params,
          page: 1,
          [param_key]: undefined,
        })
      }
      {...props}
    />
  ) : null;
}

const FILTERS = [
  {
    param_key: "safetycube",
    icon: <SafetyCubeIcon />,
    make_label: (v) => (v === "false" ? "Non" : "Oui"),
  },
  { param_key: "status", icon: <TimerSandEmpty /> },
  { param_key: "group", icon: <AccountMultiple /> },
  { param_key: "zone", icon: <Web /> },
  { param_key: "type", icon: <Shape /> },
  { param_key: "keywords", icon: <TagOutline /> },
];

export default function ActiveFiltersDisplay() {
  return (
    <Stack
      direction="row"
      alignItems="center"
      spacing={1}
      sx={{
        flex: "1 1 0%",
        minWidth: 0,
        flexWrap: "wrap",
        rowGap: "4px",
      }}
    >
      {FILTERS?.map((filter) => (
        <FilterChip key={filter.param_key} {...filter} />
      ))}
    </Stack>
  );
}
