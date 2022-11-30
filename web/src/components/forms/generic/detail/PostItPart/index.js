import React from "react";
import { Button, Box } from "@mui/material";
import { Plus } from "mdi-material-ui";

import { Part, Row } from "components/misc/PageElements";
import PostItDisplay from "./RowDisplay";
import usePostItDialog, {
  useDestroyConfirmationDialog,
} from "components/forms/generic/dialogs/PostItDialog";

export default function PostItPart({ data, form_key, ...props }) {
  const postitDialog = usePostItDialog(data?.uuid, form_key);
  const destroyDialog = useDestroyConfirmationDialog(data?.uuid, form_key);

  const postits = [...(data?.sub_data?.postits || [])];

  const handleAdd = () => {
    postitDialog.setPostIt(undefined);
    postitDialog.open();
  };

  const handleEdit = (p) => {
    postitDialog.setPostIt(p);
    postitDialog.open();
  };

  const handleDelete = (p) => {
    destroyDialog.setPostIt(p);
    destroyDialog.open();
  };

  return (
    <Part
      title={`${postits?.length || 0} PostIt${postits?.length > 1 ? "s" : ""}`}
      sx={{
        position: { lg: "fixed" },
        top: { lg: "8px" },
        right: { lg: 0 },
        width: { lg: "calc((100% - 900px) / 2 - 16px)" }, //use the remaining space to the right of form
        overflowY: { lg: "auto" },
        m: { lg: 2 },
        mt: { lg: "80px" },
        "&.Mui-expanded": {
          m: { lg: 2 },
          mt: { lg: "80px" },
        },
      }}
      defaultExpanded
      addOn={
        <Button
          size="small"
          color="secondary"
          startIcon={<Plus />}
          variant="outlined"
          onFocus={(e) => e.stopPropagation()}
          onClick={(e) => {
            e.stopPropagation();
            handleAdd();
          }}
          sx={{ mr: 1 }}
        >
          Ajouter PostIt
        </Button>
      }
      {...props}
    >
      <Box
        sx={{
          flexGrow: 1,
          maxHeight: "calc(100vh - 200px)",
          overflowY: "auto",
          mr: -2,
          pr: 2,
        }}
      >
        {postits.map((p, i) => (
          <Row key={i}>
            <PostItDisplay
              postit={p}
              span={12}
              onEdit={() => handleEdit(p)}
              onDelete={() => handleDelete(p)}
            />
          </Row>
        ))}
      </Box>
      {postitDialog.display}
      {destroyDialog.display}
    </Part>
  );
}
