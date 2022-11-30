import React, { useState } from "react";
import { Stack, Typography } from "@mui/material";
import { useAnyListQueryLoading } from "features/forms/mappings";
import { useMetaQuery } from "features/config/hooks";
import RefreshButton from "components/misc/RefreshButton";

export default function useHeader() {
  const { isLoading, refetch } = useMetaQuery();
  const isAnyTabLoading = useAnyListQueryLoading();
  const [refreshTrigger, triggerRefresh] = useState(0); //this is used to trigger current tab refresh thanks to useEffect. See FormTabContent.js

  const handleRefresh = () => {
    refetch(); //meta only
    triggerRefresh(refreshTrigger + 1);
  };

  const display = (
    <Stack direction="row" alignItems="flex-start" sx={{ mb: 2 }}>
      <Typography
        component="h2"
        variant="h4"
        color="primary"
        sx={{ flexGrow: 1 }}
      >
        {`Fiches à traiter `}
        <RefreshButton
          loading={isLoading || isAnyTabLoading}
          refresh={handleRefresh}
        />
      </Typography>
    </Stack>
  );

  return { display, refreshTrigger };
}
