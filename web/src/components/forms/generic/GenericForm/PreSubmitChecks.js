import React, { Fragment } from "react";

import { useFeatures } from "features/config/hooks";
import useMissingPictureDialog, {
  has_missing_pictures,
} from "components/forms/generic/dialogs/MissingPictureDialog";
import useAnonymousReportDialog, {
  is_anonymous_report,
} from "components/forms/generic/dialogs/AnonymousReportDialog";

export default function usePreSubmitChecks(form_props) {
  const { stripless } = useFeatures();
  const { values, onSubmit } = form_props;

  const check = (e, options) => {
    if (
      has_missing_pictures(values, stripless) &&
      !options?.force_missing_picture
    ) {
      //show missing picture dialog if any aircrafts misses strip
      missing_pictures_dialog.open(options);
    } else if (is_anonymous_report(values) && !options?.force_anonymous) {
      // if no redactors
      anonymous_dialog.open(options);
    } else {
      onSubmit(e, options);
    }
  };

  const missing_pictures_dialog = useMissingPictureDialog({
    ...form_props,
    onSubmit: check,
  });
  const anonymous_dialog = useAnonymousReportDialog({
    ...form_props,
    onSubmit: check,
  });

  const display = (
    <Fragment>
      {missing_pictures_dialog.display}
      {anonymous_dialog.display}
    </Fragment>
  );

  return { check, display };
}
