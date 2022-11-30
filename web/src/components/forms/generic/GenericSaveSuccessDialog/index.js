import React, { useEffect, Fragment } from "react";
import { useMe } from "features/auth/hooks";
import useDraftLinkDialog from "./DraftLinkDialog";
import useWarnCdsDialog from "./WarnCdsDialog";
import { useFormConfig } from "features/config/hooks";

export default function GenericSaveSuccessDialog({
  mutation_request,
  form_key,
  detail_route,
  onDialogClose,
}) {
  const { data, isSuccess } = mutation_request;
  const { is_validator } = useMe();
  const { cds_warning_enabled } = useFormConfig(form_key);
  const linkDialog = useDraftLinkDialog(
    data?.uuid,
    form_key,
    detail_route,
    onDialogClose
  );
  const warnCdsDialog = useWarnCdsDialog(onDialogClose);

  useEffect(() => {
    if (isSuccess) {
      if (data?.status?.is_draft) {
        linkDialog.open();
      } else if (
        data?.assigned_to_group?.permissions?.includes("validator") &&
        !is_validator &&
        cds_warning_enabled
      ) {
        warnCdsDialog.open();
      } else if (onDialogClose) {
        onDialogClose();
      }
    }
  }, [isSuccess, data?.status, data?.assigned_to_group]);

  return (
    <Fragment>
      {linkDialog.display}
      {warnCdsDialog.display}
    </Fragment>
  );
}
