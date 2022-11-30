import React, { useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Link,
  Divider,
  InputAdornment,
  Alert,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

import { useDialog, useForm } from "features/ui";
import formMappings from "features/forms/mappings";
import { cleanEmail } from "features/forms/shared/utils";
import ErrorBox from "components/misc/ErrorBox";
import FormTextField from "components/forms/fields/FormTextField";

export default function useDraftLinkDialog(
  uuid,
  form_key,
  route,
  onClose = () => {}
) {
  const [send_draftlink, { isLoading, isSuccess, error }] =
    formMappings[form_key].send_draftlink();
  const { isOpen, open, close } = useDialog();
  const { values, touched, handleUserInput, handleSubmit } = useForm(
    { email: "" },
    (v) => send_draftlink({ uuid, email: cleanEmail(v.email) })
  );

  const handleClose = () => {
    close();
    onClose();
  };

  useEffect(() => {
    handleClose();
  }, [isSuccess]);

  const path = route.path.replace(":pk", uuid);
  const absolute_url = `${window.location.protocol}//${window.location.host}${path}`;

  const display = (
    <Dialog open={isOpen} onClose={handleClose} maxWidth="md">
      <DialogTitle>Brouillon enregistré</DialogTitle>
      <DialogContent>
        <DialogContentText>
          {
            "Votre brouillon a bien été enregistré. Vous pouvez le reprendre en vous rendant sur cette page : "
          }
        </DialogContentText>
        <DialogContentText>
          <Link component={RouterLink} to={path}>
            {absolute_url}
          </Link>
        </DialogContentText>
        <DialogContentText component={Alert} severity="warning" sx={{ mt: 1 }}>
          Tout brouillon non validé par un CDS sera supprimé de la base de
          données dans les 48h.
        </DialogContentText>
        <Divider variant="middle" sx={{ my: 2 }} />
        <DialogContentText>
          Indiquez votre adresse professionnelle ci-dessous pour recevoir le
          lien par email :
        </DialogContentText>
        <ErrorBox errorDict={error} />
        <FormTextField
          id="email"
          label="Adresse e-mail"
          InputProps={{
            placeholder: "prenom.nom",
            endAdornment: (
              <InputAdornment position="end">
                @aviation-civile.gouv.fr
              </InputAdornment>
            ),
          }}
          values={values}
          touched={touched}
          errors={error}
          onChange={handleUserInput}
        />
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={handleClose}>
          Fermer
        </Button>
        <Button color="primary" onClick={handleSubmit} disabled={isLoading}>
          Envoyer
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
