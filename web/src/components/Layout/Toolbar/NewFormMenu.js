import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Menu, MenuItem, ListItemText, Grow } from "@mui/material";

import { useMenu } from "features/ui";
import { getRouteForNewForm } from "routes";

export default function useNewFormMenu(anchorRef, menu_list) {
  const { isOpen, anchor, open, close } = useMenu(() => anchorRef.current);

  const display = (
    <Menu
      anchorEl={anchor}
      keepMounted
      anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      MenuListProps={{ disablePadding: true }}
      PaperProps={{ evelation: 0, sx: { mt: 0.5 } }}
      TransitionComponent={Grow}
      open={isOpen()}
      onClose={close}
    >
      {menu_list?.map((form, i) => (
        <MenuItem
          key={i}
          component={RouterLink}
          onClick={close}
          to={getRouteForNewForm(form)}
        >
          <ListItemText>{form?.title}</ListItemText>
        </MenuItem>
      ))}
    </Menu>
  );

  return { display, open };
}
