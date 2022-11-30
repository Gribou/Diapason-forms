import React from "react";
import { Container, Typography, Box, Alert, Stack } from "@mui/material";

import { useMe } from "features/auth/hooks";
import { useMetaQuery } from "features/config/hooks";
import FormTabContent from "./FormTabContent";
import useHeader from "./Header";
import QueryToolbar from "./QueryToolbar";
import FormTabs from "./FormTabs";

export default function ListPage() {
  const { is_validator, is_investigator, has_all_access } = useMe();
  const metadata = useMetaQuery();
  const { data, isSuccess } = metadata;
  const { empty } = data || {};
  const header = useHeader();

  return (
    <Container maxWidth="lg" disableGutters>
      <Stack sx={{ width: "100%", m: "auto", p: { xs: 1, md: 3 } }}>
        {header.display}
        {is_validator && (
          <Alert severity="info" sx={{ mb: 2 }}>
            Les fiches marquées comme traitées (en vert) seront envoyées
            automatiquement à la subdivision concernée après la relève du Chef
            du Salle. D&apos;ici là, vous pouvez les modifier ou les supprimer.
          </Alert>
        )}

        <Box>
          {empty ? (
            isSuccess && (
              <Typography
                color="textSecondary"
                variant="subtitle1"
                gutterBottom
              >
                Aucune fiches à traiter
              </Typography>
            )
          ) : (
            <FormTabs data={data} isSuccess={isSuccess} />
          )}
        </Box>
        {!empty && isSuccess && (is_investigator || has_all_access) && (
          <QueryToolbar data={data} />
        )}
        {!empty && (
          <FormTabContent
            refreshTrigger={header?.refreshTrigger}
            sx={{ mt: 1 }}
          />
        )}
      </Stack>
    </Container>
  );
}
