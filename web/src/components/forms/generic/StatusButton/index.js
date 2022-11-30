import React, { Fragment } from "react";
import { Button, Tooltip, CircularProgress, Box } from "@mui/material";
import { MenuDown } from "mdi-material-ui";
import { useMe } from "features/auth/hooks";
import useStatusMenu from "./StatusMenu";
import { getStatusLabel, getStatusIcon, getStatusColor } from "./utils";

export default function StatusButton({
  form,
  form_key,
  status = {},
  disabled,
  loading,
  sx,
  buttonSx = [],
  ...props
}) {
  const { isError, isLoading } = status;
  const {
    status: form_status,
    assigned_to_group,
    assigned_to_person,
    available_actions,
    event_date,
  } = form;
  const { is_investigator, is_validator } = useMe();

  const menu = useStatusMenu(form, form_key);

  const isAnythingLoading = loading || isLoading || menu.isLoading;

  const disable_button =
    disabled ||
    (!is_investigator && !is_validator) ||
    (is_validator && available_actions?.length === 0) ||
    isError;

  const can_edit = !disable_button;

  const tooltip = `${form_status?.label}${
    assigned_to_group ? ` par ${assigned_to_group?.name}` : ""
  }${assigned_to_person ? ` (${assigned_to_person})` : ""}`;

  return (
    <Fragment>
      <Tooltip title={tooltip}>
        <Box component="span" sx={sx}>
          {event_date && (
            <Button
              startIcon={!isAnythingLoading && getStatusIcon(form_status)}
              endIcon={(can_edit || !disable_button) && <MenuDown />}
              sx={[
                {
                  whiteSpace: "nowrap",
                  color:
                    getStatusColor(form_status) === "inherit" &&
                    "text.secondary",
                  cursor: disable_button ? "auto" : "pointer",
                }, //show color even if disabled
                ...(Array.isArray(buttonSx) ? buttonSx : [buttonSx]),
              ]}
              color={getStatusColor(form_status)}
              disableRipple={disable_button}
              variant={can_edit ? "outlined" : "text"}
              onClick={(e) => (can_edit || !disable_button) && menu.open(e)}
              {...props}
            >
              {isAnythingLoading && (
                <CircularProgress size={16} color="inherit" sx={{ mr: 2 }} />
              )}
              {getStatusLabel(
                form_status,
                assigned_to_group,
                assigned_to_person
              )}
            </Button>
          )}
        </Box>
      </Tooltip>
      {can_edit && menu.display}
    </Fragment>
  );
}
