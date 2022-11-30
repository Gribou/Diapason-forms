import api from "api";

const action_mapping = {
  create: api.useCreateFneMutation,
  read: api.useReadFneQuery,
  update: api.useUpdateFneMutation,
  list: api.useListFneQuery,
  apply_action: api.useApplyActionToFneMutation,
  assign_to_person: api.useAssignFneToPersonMutation,
  set_keywords: api.useSetFneKeywordsMutation,
  send_draftlink: api.useSendFneDraftMailMutation,
  export: api.useExportFnePDFMutation,
  add_postit: api.useAddPostitToFneMutation,
  update_postit: api.useUpdatePostitOfFneMutation,
  destroy_postit: api.useDestroyPostitOfFneMutation,
  add_attachment: api.useAddAttachmentToFneMutation,
  destroy_attachment: api.useDestroyAttachmentOfFneMutation,
  save_to_safetycube: api.useSaveFneToSafetyCubeMutation,
  save_all_to_safetycube: api.useSaveAllFneToSafetyCubeMutation,
  refresh_safetycube_status: api.useRefreshFneSafetyCubeStatusMutation,
  send_answer: api.useSendFneAnswerMutation,
};

export default action_mapping;
