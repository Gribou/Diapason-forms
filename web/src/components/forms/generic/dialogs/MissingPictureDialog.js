import React, { useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Stack,
} from "@mui/material";
import { PhotoField } from "components/forms/fields";

import { useFeatures } from "features/config/hooks";
import useGenericPreSubmitCheckDialog from "./GenericPreSubmitCheckDialog";

export const has_missing_pictures = (values, stripless_mode) =>
  !stripless_mode &&
  values?.aircrafts?.filter(
    ({ callsign, strip, strip_url }) => callsign && !(strip || strip_url)
  )?.length > 0;

export default function useMissingPictureDialog(formProps) {
  const { stripless } = useFeatures();
  const { isOpen, open, close, handleConfirm } = useGenericPreSubmitCheckDialog(
    formProps,
    "force_missing_picture"
  );
  const { values, errors, touched, onChange } = formProps;
  const missing_pictures = !stripless
    ? values?.aircrafts?.filter(
        ({ strip, callsign, strip_url }) => callsign && !strip && !strip_url
      )
    : [];

  useEffect(() => {
    if (isOpen && missing_pictures?.length === 0) {
      //submit form once pictures have been imported
      handleConfirm();
    }
  }, [missing_pictures, isOpen]);

  const handleChange = (event, field_name, index) => {
    onChange({
      target: {
        name: "aircrafts",
        value: (values?.aircrafts || []).map((r, i) =>
          i === index ? { ...r, [field_name]: event.target.value } : r
        ),
      },
    });
  };

  const handleStripDelete = (index) => {
    const new_aircrafts = (formProps?.values?.aircrafts || []).map((r, i) =>
      i === index ? { ...r, strip_url: undefined, strip: undefined } : r
    );
    onChange({
      target: { name: "aircrafts", value: new_aircrafts },
    });
  };

  const display = (
    <Dialog open={isOpen} onClose={close}>
      <DialogTitle>Photo de strip manquante</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Merci de prendre une photo des strips pour chaque aéronef signalé :
        </DialogContentText>
        {values?.aircrafts?.map(({ callsign, strip, strip_url }, i) => (
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            key={i}
            sx={{ display: callsign && !strip && !strip_url ? "flex" : "none" }}
          >
            {callsign?.toUpperCase()}
            <PhotoField
              id="strip"
              url_id="strip_url"
              label="Strip"
              helperText="Prendre une photo du/des strips"
              onChange={(e) => handleChange(e, "strip", i)}
              onDelete={() => handleStripDelete(i)}
              onSaveMessage={`Photo du strip ${
                callsign?.toUpperCase() || ""
              } enregistrée`}
              onDeleteMessage={`Photo du strip ${
                callsign?.toUpperCase() || ""
              } supprimée`}
              values={values}
              errors={errors}
              touched={touched}
            />
          </Stack>
        ))}
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={close}>
          Annuler
        </Button>
        <Button color="primary" onClick={handleConfirm}>
          Envoyer quand même
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
