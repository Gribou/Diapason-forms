import React, { useEffect, Fragment } from "react";
import { Typography, Stack, Divider, CircularProgress } from "@mui/material";
import { useSearchParams } from "features/router";
import { useFilteredForms } from "features/forms/mappings";
import { useMetaQuery } from "features/config/hooks";
import FormPagination from "./Pagination";
import { FORM_TAB_CONFIG, getDefaultTab } from "../config";

import ErrorBox from "components/misc/ErrorBox";

function useCurrentFormData() {
  const [params] = useSearchParams();
  const { data } = useMetaQuery();
  const form_key = params?.form_key || getDefaultTab(data);
  return {
    config: FORM_TAB_CONFIG[form_key],
    ...(data?.forms[form_key] || {}),
  };
}

export default function useListTab({ refreshTrigger, ...props }) {
  const { config, relevant, count: totalCount } = useCurrentFormData();
  const { data, count, error, isLoading, refetch } = useFilteredForms();
  const RowComponent = config?.row_component;

  useEffect(() => {
    // let parent trigger this component refresh
    refetch();
  }, [refreshTrigger]);

  return (
    <Stack {...props}>
      <ErrorBox errorDict={error} sx={{ m: 1 }} />
      {isLoading && <CircularProgress sx={{ mx: "auto", my: 2 }} />}
      {(!data || !relevant || count == 0) && !isLoading && (
        <Typography
          color="textSecondary"
          variant="subtitle1"
          sx={{ p: 2, pr: 4 }}
        >
          {`Aucune ${config?.short_name}`}
        </Typography>
      )}
      {relevant && (
        <Fragment>
          <Stack divider={<Divider flexItem />}>
            {data?.map((item, i) => (
              <RowComponent data={item} key={i} />
            ))}
          </Stack>
          {!isLoading && count < totalCount && (
            <Typography
              variant="caption"
              color="textSecondary"
              sx={{ ml: "auto" }}
            >{`et ${totalCount - count} fiches filtrées`}</Typography>
          )}
          <FormPagination count={count} />
        </Fragment>
      )}
    </Stack>
  );
}
