import formMappings, {
  FNE_FORM_KEY,
  SIMI_FORM_KEY,
  BROUILLAGE_FORM_KEY,
} from "features/forms/mappings";
import FneRow from "components/forms/fne/FneRow";
import SimiRow from "components/forms/simi/SimiRow";
import BrouillageRow from "components/forms/brouillage/BrouillageRow";

export const FORM_TAB_CONFIG = {
  [FNE_FORM_KEY]: {
    short_name: "FNE",
    row_component: FneRow,
    action_mapping: formMappings[FNE_FORM_KEY],
  },
  [SIMI_FORM_KEY]: {
    short_name: "Similitude",
    row_component: SimiRow,
    action_mapping: formMappings[SIMI_FORM_KEY],
  },
  [BROUILLAGE_FORM_KEY]: {
    short_name: "Brouillage",
    row_component: BrouillageRow,
    action_mapping: formMappings[BROUILLAGE_FORM_KEY],
  },
  //NOTE : add new form tab config here
};

//first relevant tab or first tab from config
export const getDefaultTab = (metadata) =>
  Object.keys(FORM_TAB_CONFIG)?.find(
    (key) => metadata?.forms?.[key]?.relevant
  ) || Object.keys(FORM_TAB_CONFIG)[0];
