import React, { Fragment } from "react";
import { LoadingButton } from "@mui/lab";
import { FileUpload, Camera, ImageMultiple } from "mdi-material-ui";
import { isMobile } from "react-device-detect";

import { Part } from "components/misc/PageElements";
import useGalleryDialog from "components/forms/fields/GalleryField/GalleryDialog";
import { usePhotoImport } from "features/photo";
import { useMe } from "features/auth/hooks";
import { useFeatures } from "features/config/hooks";
import formMappings from "features/forms/mappings";
import AttachmentDisplay from "./RowDisplay";

export default function AttachmentPart({
  data,
  form_key,
  formProps,
  ...props
}) {
  const { is_investigator } = useMe();
  const { gallery_url } = useFeatures();
  const { onChange, values, errors } = formProps || {};
  const attachments = [...(values?.attachments || data?.attachments || [])];
  const gallery = useGalleryDialog((value) =>
    handleAdd({ target: { files: [value] } })
  );
  const handlePhotoAdd = usePhotoImport((file) =>
    handleAdd({ target: { files: [file] } })
  );
  const readOnly = !formProps && !is_investigator;
  const action_mapping = formMappings[form_key];
  const [add_attachment, { isLoading: isAddLoading }] =
    action_mapping.add_attachment();
  const [destroy_attachment, destroyStatus] =
    action_mapping.destroy_attachment();

  const handleAdd = (e) => {
    //if new form creation, store in state
    //else save directly to server
    if (data?.uuid) {
      add_attachment({ uuid: data?.uuid, file: e.target.files[0] });
    } else {
      onChange({
        target: {
          name: "attachments",
          value: [e.target.files[0], ...attachments],
        },
      });
    }
  };

  const handleDelete = ({ name, pk }) => {
    if (data?.uuid) destroy_attachment({ pk, parent: data?.uuid });
    else
      onChange({
        target: {
          name: "attachments",
          value: attachments?.filter((a) => a?.name != name),
        },
      });
  };

  const upload_button = !isMobile && (
    <Fragment>
      <input type="file" id="attachment-import" hidden onChange={handleAdd} />
      <label htmlFor="attachment-import">
        <LoadingButton
          size="small"
          color="primary"
          startIcon={<FileUpload />}
          loadingPosition="start"
          loading={isAddLoading}
          variant="outlined"
          component="span"
          onFocus={(e) => e.stopPropagation()}
          onClick={(e) => e.stopPropagation()}
          sx={{ ml: 1 }}
        >
          Importer fichier
        </LoadingButton>
      </label>
    </Fragment>
  );

  const gallery_button = gallery_url && isMobile && (
    <LoadingButton
      size="small"
      color="primary"
      variant="outlined"
      startIcon={<ImageMultiple />}
      component="span"
      onFocus={(e) => e.stopPropagation()}
      onClick={(e) => {
        e.stopPropagation();
        gallery.open();
      }}
      loadingPosition="start"
      loading={isAddLoading}
      sx={{ ml: 1 }}
    >
      Choisir photo
    </LoadingButton>
  );

  const photo_button = isMobile && (
    <Fragment>
      <input
        type="file"
        accept="image/*;capture=camera"
        hidden
        onChange={handlePhotoAdd}
        id="photo-import"
      />
      <label htmlFor="photo-import">
        <LoadingButton
          size="small"
          color="primary"
          startIcon={<Camera />}
          loadingPosition="start"
          loading={isAddLoading}
          variant="outlined"
          component="span"
          onFocus={(e) => e.stopPropagation()}
          onClick={(e) => e.stopPropagation()}
        >
          Prendre photo
        </LoadingButton>
      </label>
    </Fragment>
  );

  return (
    <Part
      title={`${attachments?.length || 0} pièce${
        attachments?.length > 1 ? "s" : ""
      } jointe${attachments?.length > 1 ? "s" : ""}`}
      expanded
      hideExpandIcon
      addOn={
        !readOnly && (
          <Fragment>
            {photo_button}
            {gallery_button}
            {upload_button}
          </Fragment>
        )
      }
      {...props}
    >
      {attachments.map((a, i) => (
        <AttachmentDisplay
          attachment={a}
          errors={errors?.attachments?.[i]}
          key={i}
          allowDelete={!readOnly && (!data?.uuid || a?.by_me)}
          onDelete={() => handleDelete(a)}
          loading={
            destroyStatus?.isLoading &&
            destroyStatus?.originalArgs?.pk === a?.pk
          }
        />
      ))}
      {gallery.display}
    </Part>
  );
}
