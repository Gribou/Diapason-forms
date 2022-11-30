import React from "react";

export default function GenericDetail({
  editMode,
  formProps,
  FormComponent,
  DisplayComponent,
  ...props
}) {
  return editMode ? (
    <FormComponent formProps={formProps} {...props} />
  ) : (
    <DisplayComponent {...props} />
  );
}
