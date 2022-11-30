import api from "api";

const useBrouillageActionMapping = {
  create: api.useCreateBrouillageMutation,
  read: api.useReadBrouillageQuery,
  update: api.useUpdateBrouillageMutation,
  list: api.useListBrouillageQuery,
  apply_action: api.useApplyActionToBrouillageMutation,
  assign_to_person: api.useAssignBrouillageToPersonMutation,
  set_keywords: api.useSetBrouillageKeywordsMutation,
  send_draftlink: api.useSendBrouillageDraftMailMutation,
  export: api.useExportBrouillagePDFMutation,
  add_postit: api.useAddPostitToBrouillageMutation,
  update_postit: api.useUpdatePostitOfBrouillageMutation,
  destroy_postit: api.useDestroyPostitOfBrouillageMutation,
  send_answer: api.useSendBrouillageAnswerMutation,
};

export default useBrouillageActionMapping;
