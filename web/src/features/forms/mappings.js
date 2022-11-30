import { useSelector } from "react-redux";
import { useSearchParams } from "features/router";
import fneMapping from "features/forms/fne/hooks";
import { FNE_TAG, FNE_FORM_KEY } from "features/forms/fne/api";
import simiMapping from "features/forms/simi/hooks";
import { SIMI_TAG, SIMI_FORM_KEY } from "features/forms/simi/api";
import {
  BROUILLAGE_TAG,
  BROUILLAGE_FORM_KEY,
} from "features/forms/brouillage/api";
import brouillageMapping from "features/forms/brouillage/hooks";
import { useAuthenticated } from "features/auth/hooks";

//NOTE : add new forms here

const mappings = {
  [FNE_FORM_KEY]: fneMapping,
  [SIMI_FORM_KEY]: simiMapping,
  [BROUILLAGE_FORM_KEY]: brouillageMapping,
};

export const tags = [FNE_TAG, SIMI_TAG, BROUILLAGE_TAG];

export { FNE_FORM_KEY, SIMI_FORM_KEY, BROUILLAGE_FORM_KEY };

export default mappings;

export const useFormByUUID = (form_key, uuid, params) => {
  //query form detail, get normalized data from slice
  //this way, the data is updated by actions like update or apply
  const is_authenticated = useAuthenticated();
  const query = mappings[form_key].read(
    { uuid, is_authenticated, params },
    { skip: !uuid }
  );
  const form = useSelector((state) => state[form_key].forms?.[uuid] || {});
  return {
    ...query,
    data: form,
  };
};

export const useFilteredForms = () => {
  const [{ form_key, ...params }] = useSearchParams();
  //query form list, replace with forms from slice
  //this way, the data is also updated by actions like update or apply action
  const formKey = form_key || FNE_FORM_KEY;
  const query = mappings[formKey]?.list(params);
  const forms_from_slice = useSelector((state) => state?.[formKey]?.forms);
  return {
    ...query,
    count: query?.data?.count || 0,
    data: query?.data?.results
      ?.filter((f) => f)
      ?.map(({ uuid }) => forms_from_slice?.[uuid] || {}),
  };
};

export const useAnyListQueryLoading = () => {
  const loading = Object.keys(mappings).map((key) =>
    useSelector((state) => state[key].loading)
  );
  return loading?.find((l) => l);
};
