import React, { Fragment } from "react";
import { Typography, Menu, MenuItem, Button, Stack } from "@mui/material";
import { MenuDown } from "mdi-material-ui";
import { useSearchParamByKey } from "features/router";
import { useMenu } from "features/ui";

export const DEFAULT_PAGE_SIZE = 10;
const SIZE_CHOICES = [5, 10, 25, 50, 100];

function useChoicesMenu(onClick) {
  const { isOpen, anchor, open, close } = useMenu();

  const handleClick = (value) => {
    onClick(value);
    close();
  };

  const display = (
    <Menu anchorEl={anchor} keepMounted open={isOpen()} onClose={close}>
      {SIZE_CHOICES?.map((choice) => (
        <MenuItem key={choice} onClick={() => handleClick(choice)}>
          {choice}
        </MenuItem>
      ))}
    </Menu>
  );

  return { open, display };
}

export default function PageSizeSelector(props) {
  const [page_size, setPageSize] = useSearchParamByKey(
    "page_size",
    DEFAULT_PAGE_SIZE
  );
  const menu = useChoicesMenu(setPageSize);

  return (
    <Fragment>
      <Stack direction="row" alignItems="center" {...props}>
        <Typography sx={{ mr: 1 }}>Eléments par page :</Typography>
        <Button endIcon={<MenuDown />} onClick={menu.open} color="inherit">
          {page_size}
        </Button>
      </Stack>
      {menu.display}
    </Fragment>
  );
}
