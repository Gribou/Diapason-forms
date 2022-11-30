import React from "react";
import Form from "./Form";
import Display from "./Display";
import GenericDetail from "components/forms/generic/detail/GenericDetail";

export default function DescriptionPart(props) {
  return (
    <GenericDetail FormComponent={Form} DisplayComponent={Display} {...props} />
  );
}
