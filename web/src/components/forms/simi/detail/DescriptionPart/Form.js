import React from "react";
import { Part } from "components/misc/PageElements";
import { FormTextField, FormCheckboxField } from "components/forms/fields";

export default function Form({ formProps, ...props }) {
  return (
    <Part
      title="Type de problème rencontré"
      defaultExpanded
      addOn={
        <FormCheckboxField
          id="with_incident"
          label="Avec incident"
          onFocus={(e) => e.stopPropagation()}
          onClick={(e) => e.stopPropagation()}
          {...formProps}
        />
      }
      {...props}
    >
      <FormTextField
        multiline
        required
        rows={6}
        id="description"
        label="Description"
        {...formProps}
      />
    </Part>
  );
}
