import api from "api";

const useSimilitudeActionMapping = {
  create: api.useCreateSimilitudeMutation,
  read: api.useReadSimilitudeQuery,
  update: api.useUpdateSimilitudeMutation,
  list: api.useListSimilitudeQuery,
  apply_action: api.useApplyActionToSimilitudeMutation,
  assign_to_person: api.useAssignSimilitudeToPersonMutation,
  set_keywords: api.useSetSimilitudeKeywordsMutation,
  send_draftlink: api.useSendSimilitudeDraftMailMutation,
  export: api.useExportSimilitudePDFMutation,
  add_postit: api.useAddPostitToSimilitudeMutation,
  update_postit: api.useUpdatePostitOfSimilitudeMutation,
  destroy_postit: api.useDestroyPostitOfSimilitudeMutation,
  save_to_safetycube: api.useSaveSimilitudeToSafetyCubeMutation,
  save_all_to_safetycube: api.useSaveAllSimilitudeToSafetyCubeMutation,
  refresh_safetycube_status: api.useRefreshSimilitudeSafetyCubeStatusMutation,
  send_answer: api.useSendSimilitudeAnswerMutation,
};

export default useSimilitudeActionMapping;
