import React, { useEffect, useState } from "react";
import {
  Dialog,
  List,
  DialogTitle,
  ListItem,
  ListItemButton,
  Checkbox,
  DialogActions,
  Button,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import { useDialog } from "features/ui";

export default function useChoicesMenu({
  choices = [],
  onClick,
  title,
  multiple,
  onCancel = () => {},
  current = "",
}) {
  const { isOpen, open, close } = useDialog();
  const [selection, setSelection] = useState();

  useEffect(() => {
    if (isOpen) {
      setSelection(current ? current?.split(",") : []);
    }
  }, [isOpen, current]);

  const handleConfirm = (confirmed, value) => {
    if (confirmed) {
      onClick(value || selection?.join(","));
    } else {
      onCancel();
    }
    close();
  };

  const handleItemClick = (value) => {
    if (multiple) {
      if (selection?.includes()) {
        setSelection(selection?.filter((s) => s !== value));
      } else {
        setSelection([...selection, value]);
      }
    } else {
      handleConfirm(true, value);
    }
  };

  const display = (
    <Dialog
      maxWidth="xs"
      fullWidth
      open={isOpen}
      onClose={() => handleConfirm(false)}
      PaperProps={{ variant: "outlined", elevation: 0 }}
    >
      <DialogTitle>{title}</DialogTitle>
      <List>
        <ListItem disablePadding>
          <ListItemButton
            role={undefined}
            onClick={() => handleConfirm(true, [])}
          >
            <ListItemIcon />
            <ListItemText primary="Tous" />
          </ListItemButton>
        </ListItem>
        {choices?.map((choice, i) => (
          <ListItem key={i} disablePadding>
            <ListItemButton
              role={undefined}
              onClick={() => handleItemClick(choice?.value || choice)}
            >
              <ListItemIcon>
                {multiple && (
                  <Checkbox
                    edge="end"
                    tabIndex={-1}
                    checked={
                      selection?.includes(choice?.value) ||
                      selection?.includes(choice)
                    }
                  />
                )}
              </ListItemIcon>
              <ListItemText primary={choice?.label || choice} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      {multiple && (
        <DialogActions>
          <Button onClick={() => handleConfirm(false)}>Fermer</Button>
          <Button color="primary" onClick={() => handleConfirm(true)}>
            Confirmer
          </Button>
        </DialogActions>
      )}
    </Dialog>
  );

  return { display, open };
}
