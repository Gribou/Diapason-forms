import React, { Fragment } from "react";
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material";

import { useSearchParams } from "features/router";
import useChoicesMenu from "./ChoicesMenu";

export default function FilterButton({
  param_key,
  choices,
  icon,
  title,
  hideBelow = 2,
  onClose,
  multiple,
}) {
  const [params, push] = useSearchParams();
  const filter = params?.[param_key];

  const setFilter = (value) => {
    push({ ...params, [param_key]: value, page: undefined });
    onClose();
  };

  const menu = useChoicesMenu({
    choices: choices?.filter((choice) => choice) || [],
    onClick: setFilter,
    title,
    onCancel: () => onClose(),
    multiple,
    current: filter,
  });

  return choices?.length >= hideBelow ? (
    <Fragment>
      <MenuItem dense onClick={menu.open}>
        <ListItemIcon>{icon}</ListItemIcon>
        <ListItemText>
          {`${title} : ${
            choices?.find((choice) => choice?.value === filter)?.label ||
            filter ||
            "Tous"
          }`}
        </ListItemText>
      </MenuItem>
      {menu.display}
    </Fragment>
  ) : null;
}
