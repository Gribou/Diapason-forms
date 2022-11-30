import React from "react";
import { Alert } from "@mui/material";
import { makePrettyErrorMessageFromDict } from "features/ui";

export default function ErrorBox({
  errorList = [],
  errorDict = {},
  noKeys,
  children,
  ...props
}) {
  const hasContent = () =>
    [...Object.values(errorDict), ...(errorList || [])]?.filter(
      (error) => error
    ).length > 0;

  const getContent = () => [
    ...errorList,
    ...makePrettyErrorMessageFromDict(errorDict, noKeys),
  ];

  return (
    hasContent() && (
      <Alert severity="error" align="justify" {...props}>
        {getContent()
          .filter((error) => error)
          .map((error, i) => (
            <div key={i}>{error}</div>
          ))}
        {children}
      </Alert>
    )
  );
}
