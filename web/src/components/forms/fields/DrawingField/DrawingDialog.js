import React, { useRef } from "react";
import { Dialog, DialogTitle, DialogActions, Button, Box } from "@mui/material";
import SignaturePad from "react-signature-canvas-react17-compatible";

import { useDialog } from "features/ui";

export default function useDrawingDialog(label, onChange) {
  const { isOpen, open, close } = useDialog();
  const pad = useRef(null);

  const clear = () => pad.current.clear();

  const save = () => {
    const canvas = pad?.current?.getCanvas();
    const rect = canvas?.getBoundingClientRect();
    onChange(
      canvas?.toDataURL("image/png", {
        width: rect?.width,
        height: rect?.height,
      })
    );
    close();
  };

  const display = (
    <Dialog open={isOpen} onClose={close} maxWidth="xl" fullWidth>
      <DialogTitle>{label}</DialogTitle>
      <SignaturePad
        ref={(ref) => {
          pad.current = ref;
        }}
        backgroundColor="#fff"
        clearOnResize={false}
        canvasProps={{
          style: { width: "100%", height: "70vh", border: "1px solid black" },
        }}
      />
      <DialogActions>
        <Button onClick={clear}>Effacer</Button>
        <Box sx={{ m: "auto" }} />
        <Button onClick={close}>Fermer</Button>
        <Button color="primary" onClick={save}>
          Enregistrer
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
