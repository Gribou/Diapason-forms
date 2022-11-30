import React, { useEffect } from "react";
import axios from "axios";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  CircularProgress,
  Grid,
  Card,
  CardActionArea,
  CardMedia,
  Alert,
  AlertTitle,
} from "@mui/material";
import { useDialog } from "features/ui";
import { useFeatures } from "features/config/hooks";
import { useGalleryQuery } from "features/gallery";

export default function useGalleryDialog(onPhotoPicked) {
  const { isOpen, open, close } = useDialog();
  const { gallery_url } = useFeatures();
  const { data, isLoading, isError, refetch, isUninitialized } =
    useGalleryQuery(gallery_url, {
      skip: !isOpen || !gallery_url,
    });

  useEffect(() => {
    if (isOpen && !isUninitialized) {
      //refresh gallery on dialog open
      refetch();
    }
  }, [isOpen]);

  const onPicked = async (picked_url) => {
    if (picked_url) {
      //fetch file from url directly without using redux state (see features/gallery)
      const filename = picked_url.substring(picked_url.lastIndexOf("/") + 1);
      const file = await axios({
        url: picked_url,
        responseType: "blob",
      }).then(
        (response) =>
          new File([response.data], filename, {
            type: "image/png",
          })
      );
      onPhotoPicked(file);
      close();
    }
  };

  const display = (
    <Dialog open={isOpen} onClose={close} maxWidth="md" fullWidth>
      <DialogTitle>Photothèque</DialogTitle>
      <DialogContent>
        {isLoading ? (
          <CircularProgress />
        ) : isError ? (
          <Alert severity="error">
            <AlertTitle>Le chargement de la photothèque a échoué.</AlertTitle>
            Utilisez le bouton &apos;Appareil photo&apos; pour prendre une photo
            directement.
          </Alert>
        ) : data?.length === 0 ? (
          <Alert severity="info" variant="outlined">
            <AlertTitle>Aucune photo dans la photothèque</AlertTitle>
            Utilisez le bouton Appareil photo pour prendre une nouvelle image.
          </Alert>
        ) : (
          <Grid container justify="flex-start" alignItems="stretch">
            {(data || []).map(({ file }, i) => (
              <Grid item xs={4} key={i} sx={{ p: 1 }}>
                <Card
                  sx={{
                    m: 1,
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  <CardActionArea
                    onClick={() => onPicked(file)}
                    sx={{ flexGrow: 1 }}
                  >
                    <CardMedia
                      component="img"
                      image={file}
                      sx={{ width: "100%" }}
                    />
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={close}>
          Annuler
        </Button>
      </DialogActions>
    </Dialog>
  );

  return { display, open };
}
