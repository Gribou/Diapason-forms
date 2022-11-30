import React, { Fragment } from "react";
import {
  Button,
  Tooltip,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import {
  SortCalendarAscending,
  SortCalendarDescending,
  SortAlphabeticalAscending,
  SortAlphabeticalDescending,
  MenuDown,
} from "mdi-material-ui";
import { useSearchParams } from "features/router";
import { useMenu } from "features/ui";

const DATE_ASC = "date";
const DATE_DESC = "-date";
const REF_DESC = "-ref";
const REF_ASC = "ref";

function useSortMenu() {
  const [params, push] = useSearchParams();
  const { isOpen, anchor, open, close } = useMenu();

  const handleClick = (value) => {
    push({ ...params, sort: value, page: undefined });
    close();
  };

  const display = (
    <Menu anchorEl={anchor} keepMounted open={isOpen()} onClose={close}>
      <MenuItem onClick={() => handleClick(REF_ASC)}>
        <ListItemIcon>
          <SortAlphabeticalAscending />
        </ListItemIcon>
        <ListItemText>Alphabétique (référence)</ListItemText>
      </MenuItem>
      <MenuItem onClick={() => handleClick(REF_DESC)}>
        <ListItemIcon>
          <SortAlphabeticalDescending />
        </ListItemIcon>
        <ListItemText>Anti-alphabétique (référence)</ListItemText>
      </MenuItem>
      <MenuItem onClick={() => handleClick(DATE_ASC)}>
        <ListItemIcon>
          <SortCalendarAscending />
        </ListItemIcon>
        <ListItemText>Chronologique</ListItemText>
      </MenuItem>
      <MenuItem onClick={() => handleClick(DATE_DESC)}>
        <ListItemIcon>
          <SortCalendarDescending />
        </ListItemIcon>
        <ListItemText>Anti-chronologique</ListItemText>
      </MenuItem>
    </Menu>
  );

  return { display, open };
}

export default function useSortButton(props) {
  const [{ sort }] = useSearchParams();
  const menu = useSortMenu();

  const get_icon = () => {
    if (sort === DATE_ASC) return <SortCalendarAscending />;
    if (sort === DATE_DESC) return <SortCalendarDescending />;
    if (sort === REF_DESC) return <SortAlphabeticalDescending />;
    return <SortAlphabeticalAscending />;
  };

  const get_text = () => {
    if (sort === DATE_ASC) return "Asc";
    if (sort === DATE_DESC) return "Desc";
    if (sort === REF_DESC) return "Asc";
    return "Desc";
  };

  return (
    <Fragment>
      <Tooltip title="Changer l'ordre">
        <Button
          variant="outlined"
          color="primary"
          onClick={menu.open}
          {...props}
          size="small"
          startIcon={get_icon()}
          endIcon={<MenuDown />}
        >
          {get_text()}
        </Button>
      </Tooltip>
      {menu.display}
    </Fragment>
  );
}
