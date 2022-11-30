import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";

import { useDialog } from "features/ui";

export default function usePhotoPreviewDialog(img_url, props) {
  const { isOpen, open, close } = useDialog();

  const is_url = (url) =>
    url?.startsWith("blob:") ||
    url?.startsWith("http") ||
    url?.startsWith("data:");

  const display = (
    <Dialog open={isOpen} onClose={close} {...props}>
      <DialogTitle>Aperçu</DialogTitle>
      <DialogContent>
        <img
          src={is_url(img_url) ? img_url : `data:image/png;base64,${img_url}`}
          style={{ width: "100%", height: "98%", objectFit: "contain" }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={close}>Fermer</Button>
      </DialogActions>
    </Dialog>
  );
  return { display, open };
}
