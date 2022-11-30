import React, { Fragment } from "react";
import { Menu, Divider, Box } from "@mui/material";
import {
  Account,
  NoteOutline,
  FileExportOutline,
  TagOutline,
  EmailFast,
} from "mdi-material-ui";
import { useMenu } from "features/ui";
import { useMe } from "features/auth/hooks";
import { useFormConfig } from "features/config/hooks";
import formMappings from "features/forms/mappings";
import { ActionMenuItem } from "components/misc/ActionMenuItem";
import useKeywordsDialog from "./KeywordsDialog";
import useAssignPersonDialog from "./AssignPersonDialog";
import usePostItDialog from "components/forms/generic/dialogs/PostItDialog";
import useExportDialog from "./ExportDialog";
import { getStatusIcon } from "./utils";
import SafetyCubeIcon from "components/logos/SafetyCubeIcon";
import useSendAnswerDialog from "./SendAnswerDialog";

const make_form_action = ({ action, mutation, form, is_investigator }) => ({
  label: action?.label,
  action_name: "apply_action",
  icon: getStatusIcon(action?.next_status),
  payload: {
    uuid: form?.uuid,
    is_draft: form?.status?.is_draft,
    action,
  },
  mutation,
  enabled: is_investigator || action?.next_group === form.assigned_to_group?.pk,
});
//show all actions to investigator
//show only own actions to validator. transfer will be done automatically

export default function useStatusMenu(form, form_key) {
  const { uuid, available_actions, safetycube, status, answer } = form;
  const { is_investigator } = useMe();
  const { isOpen, anchor, open, close } = useMenu();
  const { safetycube_enabled } = useFormConfig(form_key);
  const apply_mutation = formMappings[form_key].apply_action();
  const extra_actions = [
    {
      action_name: "save_to_safetycube",
      label: "Enregistrer dans SafetyCube",
      icon: <SafetyCubeIcon />,
      mutation: formMappings[form_key]?.save_to_safetycube?.(),
      payload: { uuid: form?.uuid },
      enabled: is_investigator && safetycube_enabled && !safetycube?.reference,
    },
    {
      action_name: "send_answer",
      label: "Envoyer la réponse",
      icon: <EmailFast />,
      dialog: useSendAnswerDialog(uuid, form_key, answer || {}),
      enabled: is_investigator && status?.is_done,
    },
    {
      action_name: "assign_to_person",
      label: "Attribuer à une personne",
      icon: <Account />,
      dialog: useAssignPersonDialog(uuid, form_key),
      enabled: is_investigator,
    },
    {
      action_name: "add_postit",
      label: "Ajouter un PostIt",
      icon: <NoteOutline />,
      dialog: usePostItDialog(uuid, form_key),
      enabled: is_investigator,
    },
    {
      action_name: "set_keywords",
      label: "Modifier les mots-clés",
      icon: <TagOutline />,
      dialog: useKeywordsDialog(uuid, form_key, form?.keywords),
      enabled: is_investigator,
    },
    {
      action_name: "export",
      label: "Exporter en PDF",
      icon: <FileExportOutline />,
      dialog: useExportDialog(uuid, form_key),
      enabled: is_investigator,
    },
    {
      action_name: "refresh_safetycube_status",
      label: "Actualiser l'état SafetyCube",
      icon: <SafetyCubeIcon />,
      enabled: is_investigator && safetycube_enabled && safetycube?.reference,
      mutation: formMappings[form_key]?.refresh_safetycube_status?.(),
      payload: { uuid: form?.uuid },
    },
  ]?.filter(
    ({ action_name, enabled }) =>
      enabled && formMappings[form_key]?.[action_name]
  );

  const isAnythingLoading =
    apply_mutation?.[1]?.isLoading ||
    extra_actions.some(
      ({ mutation, dialog, enabled }) =>
        enabled && (mutation?.[1]?.isLoading || dialog?.isLoading)
    );

  const display = (
    <Fragment>
      <Menu
        anchorEl={anchor}
        keepMounted
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        open={isOpen()}
        onClose={close}
      >
        {extra_actions?.map((action, i) => (
          <ActionMenuItem key={i} {...action} onClose={close} />
        ))}
        {extra_actions?.length > 0 && <Divider />}
        {available_actions
          ?.map((action) =>
            make_form_action({
              action,
              mutation: apply_mutation,
              is_investigator,
              form,
            })
          )
          ?.filter(({ enabled }) => enabled)
          ?.map((action, i) => (
            <ActionMenuItem key={i} {...action} onClose={close} />
          ))}
      </Menu>
      {extra_actions
        ?.filter(({ dialog }) => dialog)
        .map(({ dialog }, i) => (
          <Box key={i}>{dialog?.display}</Box>
        ))}
    </Fragment>
  );

  return { display, open, isLoading: isAnythingLoading };
}
