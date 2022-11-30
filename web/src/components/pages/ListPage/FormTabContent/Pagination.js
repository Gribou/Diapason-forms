import React from "react";
import { Pagination, PaginationItem, Stack } from "@mui/material";
import { useSearchParams } from "features/router";
import PageSizeSelector, { DEFAULT_PAGE_SIZE } from "./PageSizeSelector";

export default function FormPagination({ count }) {
  const [params, push] = useSearchParams();
  const page = parseInt(params?.page, 10) || 1;
  const page_size = parseInt(params?.page_size, 10) || DEFAULT_PAGE_SIZE;

  const nb_pages = () => Math.floor((count - 1) / page_size) + 1;

  const setPage = (value) => push({ ...params, page: value });

  return (
    <Stack
      direction="row"
      sx={{ mt: 1 }}
      justifyContent="space-between"
      alignItems="center"
    >
      <PageSizeSelector
        sx={{ display: params?.page_size || count > 5 ? "flex" : "none" }}
      />
      <Pagination
        count={nb_pages()}
        page={page}
        color="primary"
        sx={{
          display: nb_pages() > 1 ? "block" : "none",
        }}
        onChange={(e, value) => setPage(value)}
        renderItem={(item) => (
          <PaginationItem
            {...item}
            variant={item.selected ? "outlined" : "text"}
          />
        )}
      />
    </Stack>
  );
}
