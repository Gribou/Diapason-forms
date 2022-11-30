import React from "react";
import { Container, Typography, Stack } from "@mui/material";
import { Part, Row, Cell } from "components/misc/PageElements";
import RefreshButton from "components/misc/RefreshButton";
import ErrorBox from "components/misc/ErrorBox";

import { useStatsQuery } from "features/stats/hooks";
import { useFeatures } from "features/config/hooks";
import MonthBarGraph from "./MonthBarGraph";

export default function StatsPage() {
  const { show_stats } = useFeatures();
  const { data: stats, isLoading, refetch } = useStatsQuery();

  return show_stats ? (
    <Container maxWidth="md" disableGutters>
      <Stack sx={{ m: "auto", p: { xs: 1, md: 3 } }}>
        <Typography component="h2" variant="h4" color="primary" sx={{ p: 2 }}>
          {"Statistiques d'utilisation d'eFNE"}
          <RefreshButton
            loading={isLoading}
            refresh={refetch}
            sx={{ verticalAlign: "baseline", ml: 1 }}
          />
        </Typography>
        <Part expanded hideExpandIcon sx={{ pt: 1 }}>
          <Row>
            <Cell span>
              <Typography gutterBottom paragraph>
                {`Au total, ${
                  stats?.totals?.all || 0
                } fiches ont été saisies dans eFNE dont ${
                  (stats?.totals?.all || 0) - (stats?.totals?.QSS || 0)
                } par la salle de contrôle.`}
              </Typography>
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <MonthBarGraph
                loading={isLoading}
                data={stats?.form_graph}
                colorOffset={4}
                title="Fiches enregistrées par type (toutes sources)"
              />
            </Cell>
          </Row>
          <Row>
            <Cell span>
              <MonthBarGraph
                loading={isLoading}
                data={stats?.category_graph}
                excludedCategories={["QSS", "Global"]}
                title="Fiches enregistrées par la salle de contrôle"
              />
            </Cell>
          </Row>
        </Part>
      </Stack>
    </Container>
  ) : (
    <ErrorBox errorList={["Cette page n'est pas disponible"]} />
  );
}
