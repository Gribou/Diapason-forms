import React from "react";
import {
  TimerSandEmpty,
  HeadCogOutline,
  CheckboxMarkedCircleOutline,
  FileDocumentEditOutline,
  DotsHorizontal,
  Delete,
} from "mdi-material-ui";

export function getStatusIcon(status) {
  if (status?.is_draft) return <FileDocumentEditOutline />;
  if (status?.is_waiting) return <TimerSandEmpty />;
  if (status?.is_in_progress) return <HeadCogOutline />;
  if (status?.is_done) return <CheckboxMarkedCircleOutline />;
  if (status?.is_to_be_deleted) return <Delete />;
  return <DotsHorizontal />;
}

export const getStatusLabel = (status, assigned_to_group, assigned_to_person) =>
  assigned_to_person || assigned_to_group?.name || status?.label || "";

export function getStatusColor(status) {
  if (status?.is_draft || status?.is_to_be_deleted) return "inherit";
  if (status?.is_waiting) return "warning";
  if (status?.is_in_progress) return "info";
  if (status?.is_done) return "success";
  return "error";
}
