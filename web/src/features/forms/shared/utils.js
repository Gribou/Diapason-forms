export const cleanEmail = (email) =>
  email?.includes("@") || !email ? email : `${email}@aviation-civile.gouv.fr`;

export const genericMakeFormPretty = (data) => {
  //format form values before they are sent to API
  //- status, assigned_to and actions are readonly
  // let backend raise errors, just send pretty data
  return {
    ...data,
    status: undefined,
    available_actions: undefined,
    assigned_to_group: undefined,
    keywords: Array.isArray(data.keywords)
      ? data?.keywords
          ?.filter((word) => word)
          ?.join(" ")
          ?.trim()
      : data?.keywords?.trim(),
  };
};

export const capitalize = (string) =>
  string
    ?.split(" ")
    .map(([initial, ...rest]) =>
      [initial?.toUpperCase() || "", ...rest].join("")
    )
    .join(" ");
