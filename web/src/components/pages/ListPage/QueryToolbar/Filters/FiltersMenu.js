import React from "react";
import { Divider, Menu } from "@mui/material";
import {
  Web,
  Shape,
  TimerSandEmpty,
  AccountMultiple,
  TagOutline,
} from "mdi-material-ui";
import { useMenu } from "features/ui";
import SafetyCubeIcon from "components/logos/SafetyCubeIcon";
import CancelButton from "./CancelButton";
import FilterButton from "./FilterButton";

export default function useFiltersMenu(current_meta) {
  const { isOpen, anchor, open, close } = useMenu();

  const display = (
    <Menu anchorEl={anchor} keepMounted open={isOpen()} onClose={close}>
      <FilterButton
        param_key="safetycube"
        choices={current_meta?.safetycube || []}
        icon={<SafetyCubeIcon />}
        title="Référence SafetyCube"
        onClose={close}
      />
      <FilterButton
        param_key="status"
        choices={current_meta?.statuses || []}
        icon={<TimerSandEmpty />}
        title="Etat de traitement"
        onClose={close}
        multiple
      />
      <FilterButton
        param_key="group"
        choices={current_meta?.assigned_to || []}
        icon={<AccountMultiple />}
        title="Entité responsable"
        onClose={close}
        multiple
      />
      <FilterButton
        param_key="zone"
        choices={current_meta?.zones || []}
        icon={<Web />}
        title="Zone de qualification"
        onClose={close}
        multiple
      />
      <FilterButton
        param_key="type"
        choices={current_meta?.event_types || []}
        icon={<Shape />}
        title="Type d'évènement"
        onClose={close}
        multiple
      />
      <FilterButton
        param_key="keywords"
        choices={current_meta?.keywords || []}
        icon={<TagOutline />}
        title="Mot-clé"
        hideBelow={1}
        onClose={close}
        multiple
      />
      <Divider />
      <CancelButton onClose={close} />
    </Menu>
  );

  return { display, open };
}
