export const makeTechActionsToDo = (fne) =>
  fne?.tech_event
    ?.map(({ actions }) => actions)
    ?.flat()
    ?.filter((v, i, a) => a.findIndex((t) => t.pk === v.pk) === i) || [];

export const techActionsComplete = (done, to_do) => {
  if (to_do?.length === 0) return true;
  //all actions that should be done have been done
  const pk_done = done?.map(({ pk }) => pk);
  const pk_to_do = to_do?.map(({ pk }) => pk);
  return (
    pk_done?.length === pk_to_do?.length &&
    pk_to_do?.every((pk) => pk_done?.find((p) => p === pk))
  );
};
