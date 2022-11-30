import React from "react";
import {
  Typography,
  Tooltip,
  IconButton,
  CircularProgress,
} from "@mui/material";
import { Download, Delete, AlertCircleOutline } from "mdi-material-ui";
import Mime from "mime/lite";

import { Row, Cell } from "components/misc/PageElements";
import ShowPhotoButton from "components/forms/fields/PhotoField/ShowPhotoButton";
import { makePrettyErrorMessageFromDict } from "features/ui";

export function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["octets", "Ko", "Mo", "Go", "To"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

export const ellipsize = (str) =>
  str && (str.length > 100 ? "..." + str.slice(-100) : str);

export default function AttachmentDisplay({
  attachment,
  errors,
  allowDelete,
  onDelete,
  loading,
  ...props
}) {
  const { name, file_url, size, author, type } = attachment;
  //if already uploaded from server : file_url, size, author, type, by_me
  //if not uploaded yet : name, file, size as bytes

  const filename = file_url?.split("/").reverse()[0] || name;
  const filetype = type || Mime.getType(name);
  const pretty_size = Number.isInteger(size) ? formatBytes(size) : size;

  const preview_button = filetype?.includes("image/") ? (
    <ShowPhotoButton url={file_url} file={file_url ? undefined : attachment} />
  ) : (
    <Tooltip title="Télécharger la pièce jointe">
      <IconButton
        color="primary"
        size="small"
        component="a"
        href={file_url}
        target="_blank"
        rel="noreferrer"
        download={file_url?.split(".")[-1]}
      >
        <Download />
      </IconButton>
    </Tooltip>
  );

  return (
    <Row {...props}>
      {errors && (
        <Cell>
          <AlertCircleOutline color="error" />
        </Cell>
      )}
      <Cell span alignItems="flex-start" direction="column">
        <Typography>{ellipsize(filename) || "<vide>"}</Typography>
        {errors && (
          <Typography color="error" variant="caption">
            {makePrettyErrorMessageFromDict(errors)}
          </Typography>
        )}
      </Cell>
      {author && (
        <Cell span={3} alignItems="center" justifyContent="flex-end">
          <Typography color="textSecondary" variant="caption">
            {`par ${author}`}
          </Typography>
        </Cell>
      )}
      <Cell span={1} alignItems="center" justifyContent="flex-end">
        <Typography color="textSecondary" variant="caption" noWrap>
          {pretty_size}
        </Typography>
      </Cell>
      <Cell alignItems="center">
        {preview_button}
        <Tooltip title="Supprimer la pièce jointe">
          <span>
            <IconButton
              color="error"
              size="small"
              onClick={onDelete}
              disabled={!allowDelete || loading}
            >
              {loading ? (
                <CircularProgress size="24px" color="error" />
              ) : (
                <Delete />
              )}
            </IconButton>
          </span>
        </Tooltip>
      </Cell>
    </Row>
  );
}
