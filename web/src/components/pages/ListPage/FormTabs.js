import React from "react";
import { Tab, Tabs, Stack, Box } from "@mui/material";
import { useSearchParams } from "features/router";

import { WarningBadge, AlarmBadge } from "./Badges";
import { getDefaultTab, FORM_TAB_CONFIG } from "./config";

export function useTab(default_tab) {
  const [params, push] = useSearchParams();
  const tab = params?.form_key || default_tab;

  const onChange = (e, new_tab) =>
    push({
      form_key: new_tab,
    });

  return { tab, onChange };
}

export default function FormTabs({ data = {}, isSuccess }) {
  const { forms } = data;
  const default_tab = getDefaultTab(data);
  const { tab, onChange } = useTab(default_tab);

  return (
    <Tabs
      value={tab}
      onChange={onChange}
      indicatorColor="primary"
      sx={{ borderBottom: isSuccess ? 1 : 0, borderColor: "divider" }}
    >
      {Object.entries(forms || {})
        ?.filter(([, { relevant }]) => relevant)
        ?.map(([form_key, form]) => (
          <Tab
            key={form_key}
            label={
              <Stack
                direction="row"
                sx={{ flexGrow: 1, width: "100%" }}
                alignItems="center"
              >
                <Box
                  component="span"
                  sx={{ flexGrow: 1, mx: 2 }}
                >{`${form?.count} ${FORM_TAB_CONFIG[form_key]?.short_name} `}</Box>
                {form?.warnings > 0 && (
                  <WarningBadge content={form?.warnings || 0} />
                )}
                {form?.alarms > 0 && <AlarmBadge content={form?.alarms || 0} />}
              </Stack>
            }
            value={form_key}
            disabled={!form?.count || false}
          />
        ))}
    </Tabs>
  );
}
