import React, { Fragment } from "react";
import {
  Tooltip,
  IconButton,
  CircularProgress,
  Menu,
  Box,
} from "@mui/material";
import { DotsVertical } from "mdi-material-ui";
import { useMenu } from "features/ui";
import formMappings from "features/forms/mappings";
import { useFormConfig } from "features/config/hooks";
import { useMe } from "features/auth/hooks";
import SafetyCubeIcon from "components/logos/SafetyCubeIcon";
import { ActionMenuItem } from "components/misc/ActionMenuItem";

function useGlobalMenu(form_key) {
  const { is_investigator } = useMe();
  const { safetycube_enabled } = useFormConfig(form_key);
  const { isOpen, anchor, open, close } = useMenu();

  const actions = [
    {
      action_name: "save_all_to_safetycube",
      label: "Tout enregistrer dans SafetyCube",
      mutation: formMappings[form_key]?.save_all_to_safetycube?.(),
      icon: <SafetyCubeIcon />,
      enabled: is_investigator && safetycube_enabled,
    },
  ];

  const isLoading = actions.some(
    ({ mutation, dialog, enabled }) =>
      enabled && (mutation?.[1]?.isLoading || dialog?.isLoading)
  );

  const display = (
    <Fragment>
      <Menu
        anchorEl={anchor}
        keepMounted
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        open={isOpen()}
        onClose={close}
      >
        {actions?.map((action, i) => (
          <ActionMenuItem key={i} {...action} onClose={close} />
        ))}
      </Menu>
      {actions
        ?.filter(({ dialog }) => dialog)
        .map(({ dialog }, i) => (
          <Box key={i}>{dialog?.display}</Box>
        ))}
    </Fragment>
  );

  return {
    display,
    open,
    isLoading,
    disabled: actions.some(({ enabled }) => !enabled),
  };
}

export default function GlobalMenuButton({ form_key, ...props }) {
  const menu = useGlobalMenu(form_key);

  return (
    <Fragment>
      <Tooltip title="Actions concernant toutes les fiches">
        <span>
          <IconButton
            disabled={menu.isLoading || menu.disabled}
            onClick={menu.open}
            size="small"
            {...props}
          >
            {menu.isLoading ? (
              <CircularProgress size="24px" />
            ) : (
              <DotsVertical />
            )}
          </IconButton>
        </span>
      </Tooltip>
      {menu.display}
    </Fragment>
  );
}
