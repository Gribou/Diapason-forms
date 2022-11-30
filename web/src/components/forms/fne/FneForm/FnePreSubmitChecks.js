import React, { Fragment } from "react";

import { useMe } from "features/auth/hooks";
import usePreSubmitChecks from "components/forms/generic/GenericForm/PreSubmitChecks";
import useTechActionsDialog from "./TechActionsDialog";
import { techActionsComplete, makeTechActionsToDo } from "../utils";

export default function useFnePreSubmitChecks(form_props) {
  const me = useMe();
  const { values } = form_props;
  const generic = usePreSubmitChecks(form_props);

  const check = (e, options) => {
    if (
      options?.proceed &&
      !options?.force_tech_actions &&
      me?.is_validator &&
      !techActionsComplete(
        values?.tech_actions_done,
        makeTechActionsToDo(values)
      )
    ) {
      //show tech action reminder if validator is submitting
      tech_actions_dialog.open(options);
    } else {
      generic.check(e, options);
    }
  };

  const tech_actions_dialog = useTechActionsDialog({
    ...form_props,
    onSubmit: check,
  });

  const display = (
    <Fragment>
      {tech_actions_dialog.display}
      {generic.display}
    </Fragment>
  );

  return { check, display };
}
