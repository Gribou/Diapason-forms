import React from "react";
import moment from "moment";
import { useNavigate, useLocation } from "react-router-dom";
import { Typography, ButtonBase, Stack } from "@mui/material";

import StatusButton from "components/forms/generic/StatusButton";
import { DATETIME_DISPLAY_FORMAT } from "constants/config";
import { useMe } from "features/auth/hooks";
import { useFeatures, useFormConfig } from "features/config/hooks";

import RowAvatar from "./RowAvatar";
import PostItBadge from "./PostItBadge";
import AttachmentBadge from "./AttachmentBadge";
import TagChip from "./TagChip";
import SafetyCubeButton from "../SafetyCubeButton";

export { default as ErrorChip } from "./ErrorChip";
export { default as NormalChip } from "./NormalChip";
export { default as WarningChip } from "./WarningChip";

export default function FormListRow({
  data,
  detailRoute,
  subtitle,
  noAvatar,
  children,
  form_key,
  loading,
  ...props
}) {
  const navigate = useNavigate();
  const { search } = useLocation();
  //if there isn't any zones in config, do not show RowAvatar
  const { has_zones } = useFeatures();
  const { safetycube_enabled } = useFormConfig(form_key);
  const { groups, has_all_access } = useMe();
  const {
    uuid,
    assigned_to_group,
    event_date,
    sub_data,
    attachments,
    zones,
    keywords,
  } = data || {};
  const clean_keywords = keywords
    ?.trim()
    ?.split(" ")
    ?.filter((word) => word);

  const for_me = Boolean(
    groups?.find(({ pk }) => assigned_to_group?.pk === pk)
  );

  const postit_count = sub_data?.postits?.length || 0;
  const attachment_count = attachments?.length || 0;

  return (
    <Stack direction="row" alignItems="center">
      <Stack
        direction="row"
        component={ButtonBase}
        onClick={() =>
          navigate({
            pathname: detailRoute.path.replace(":pk", uuid),
            search,
          })
        }
        justifyContent="flex-start"
        sx={{ py: 1, flexGrow: 1, flex: "1 1 0%", minWidth: 0 }}
        {...props}
      >
        {!noAvatar && has_zones && <RowAvatar zones={zones} sx={{ mr: 2 }} />}
        <Stack sx={{ mr: 2, alignItems: "flex-start" }}>
          <Typography color="inherit" variant="subtitle2">
            {moment(event_date).utc().format(DATETIME_DISPLAY_FORMAT)}
          </Typography>
          <Typography variant="caption" color="textSecondary">
            {subtitle}
          </Typography>
        </Stack>
        <Stack
          direction="row"
          alignItems="center"
          sx={{ flex: "1 1 0%", minWidth: 0, flexWrap: "wrap", rowGap: "4px" }}
        >
          {children}
          {clean_keywords?.map((word, i) => (
            <TagChip
              keyword={word}
              keywords={clean_keywords}
              key={i}
              uuid={uuid}
              form_key={form_key}
            />
          ))}
        </Stack>
      </Stack>
      {postit_count > 0 && <PostItBadge count={postit_count} sx={{ mx: 1 }} />}
      {attachment_count > 0 && (
        <AttachmentBadge count={attachment_count} sx={{ mx: 1 }} />
      )}
      {safetycube_enabled && (
        <SafetyCubeButton {...data?.safetycube} sx={{ mx: 1 }} />
      )}
      <StatusButton
        form={data}
        form_key={form_key}
        loading={loading}
        size="small"
        buttonSx={{ minWidth: "180px", ml: 1 }}
        disabled={!has_all_access && !for_me}
      />
    </Stack>
  );
}
