import React, { Fragment } from "react";
import { Typography } from "@mui/material";
import ShowPhotoButton from "./ShowPhotoButton";
import DownloadPhotoButton from "./DownloadPhotoButton";

export default function PhotoDisplay({ url, title }) {
  return (
    <Fragment>
      {title && (
        <Typography
          variant="subtitle2"
          sx={{ mr: 2 }}
        >{`${title} :`}</Typography>
      )}
      <ShowPhotoButton url={url} sx={{ verticalAlign: "baseline" }} />
      <DownloadPhotoButton url={url} sx={{ verticalAlign: "baseline" }} />
    </Fragment>
  );
}
