import React from "react";
import MultiRowForm from "./MultiRowForm";
import MultiRowDisplay from "./MultiRowDisplay";

export default function MultiRowDetail({
  item_name,
  item_key,
  items,
  editMode,
  formProps,
  SubFormComponent,
  SubDisplayComponent,
  additionalFormProps,
  additionalDisplayProps,
  ...props
}) {
  return editMode ? (
    <MultiRowForm
      formProps={formProps}
      item_name={item_name}
      item_key={item_key}
      SubFormComponent={SubFormComponent}
      {...additionalFormProps}
      {...props}
    />
  ) : (
    <MultiRowDisplay
      items={items}
      item_name={item_name}
      RowComponent={SubDisplayComponent}
      {...additionalDisplayProps}
      {...props}
    />
  );
}
