import React from "react";
import moment from "moment-timezone";
import {
  Box,
  Typography,
  Divider,
  Tooltip,
  IconButton,
  Stack,
} from "@mui/material";
import { lighten } from "@mui/system";
import { Pencil, Delete } from "mdi-material-ui";
import { Cell } from "components/misc/PageElements";

import { LOCAL_DATETIME_DISPLAY_FORMAT } from "constants/config";

export default function PostItDisplay({ postit, onEdit, onDelete, ...props }) {
  const { content, author, creation_date, by_me, loading } = postit;

  return (
    <Cell span {...props}>
      <Box
        sx={{
          border: 1,
          borderRadius: 5,
          borderColor: by_me ? "secondary.light" : "divider",
          flexGrow: 1,
          whiteSpace: "pre-wrap",
          backgroundColor: (t) =>
            by_me ? lighten(t.palette.secondary.light, 0.9) : undefined,
          m: 1,
          mr: by_me ? 1 : 8,
          ml: by_me ? 8 : 1,
        }}
      >
        <Typography variant="body2" align="justify" sx={{ m: 2 }}>
          {content || "?"}
        </Typography>
        <Divider sx={{ mt: 2 }} />
        <Stack
          direction="row"
          sx={{ mx: 1, minHeight: "34px" }}
          alignItems="center"
        >
          <Typography
            variant="caption"
            component="div"
            color="textSecondary"
            sx={{ flexGrow: 1, mx: 1 }}
          >
            {`${author}, le ${moment(creation_date).format(
              LOCAL_DATETIME_DISPLAY_FORMAT
            )}` || "?"}
          </Typography>
          {postit.by_me && (
            <Tooltip title="Modifier le postIt">
              <IconButton
                onClick={() => onEdit(postit)}
                size="small"
                disabled={loading}
              >
                <Pencil />
              </IconButton>
            </Tooltip>
          )}
          {postit.by_me && (
            <Tooltip title="Supprimer le postIt">
              <IconButton
                size="small"
                onClick={() => onDelete(postit?.pk)}
                disabled={loading}
                color="error"
              >
                <Delete />
              </IconButton>
            </Tooltip>
          )}
        </Stack>
      </Box>
    </Cell>
  );
}
