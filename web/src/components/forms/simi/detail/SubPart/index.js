import React, { Fragment } from "react";
import { Button, CircularProgress } from "@mui/material";
import { Pencil, InformationOutline } from "mdi-material-ui";

import { useMe } from "features/auth/hooks";
import { useFormConfig } from "features/config/hooks";
import formMappings, { SIMI_FORM_KEY } from "features/forms/mappings";
import { Part, Row, LabelCell, ValueCell } from "components/misc/PageElements";
import SafetyCubeButton from "components/forms/generic/SafetyCubeButton";
import useSubDataDialog from "./SubDataDialog";

export default function SubPart({ data }) {
  const { sub_data, keywords, safetycube } = data;
  const { has_all_access } = useMe();
  const { safetycube_enabled } = useFormConfig(SIMI_FORM_KEY);
  const [update, { isLoading }] = formMappings[SIMI_FORM_KEY].update();

  const onSubmit = (values) =>
    update({ uuid: data?.uuid, is_authenticated: true, ...values });

  const editDialog = useSubDataDialog(data, onSubmit);

  return (
    <Part
      title="Enquête"
      addOn={
        <Fragment>
          {safetycube_enabled ? (
            <SafetyCubeButton {...safetycube} showRef sx={{ mr: 1 }} />
          ) : (
            sub_data?.inca_number && (
              <Button
                size="small"
                disabled
                startIcon={<InformationOutline />}
                sx={{ mr: 1 }}
              >{`INCA ${sub_data?.inca_number}`}</Button>
            )
          )}
          {has_all_access && (
            <Button
              size="small"
              color="primary"
              startIcon={!isLoading && <Pencil />}
              variant="outlined"
              onFocus={(e) => e.stopPropagation()}
              onClick={(e) => {
                e.stopPropagation();
                editDialog.open();
              }}
              sx={{ mr: 1 }}
            >
              {isLoading && (
                <CircularProgress
                  size={16}
                  color="inherit"
                  style={{ marginRight: 8 }}
                />
              )}
              Modifier
            </Button>
          )}
        </Fragment>
      }
      defaultExpanded
    >
      <Row>
        <LabelCell label="Numéro INCA" />
        <ValueCell value={sub_data?.inca_number} />
      </Row>
      <Row>
        <LabelCell label="Mots-clés" />
        <ValueCell value={keywords} />
      </Row>
      {editDialog.display}
    </Part>
  );
}
