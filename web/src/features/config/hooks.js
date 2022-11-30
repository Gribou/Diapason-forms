import api from "api";
import {
  BROUILLAGE_FORM_KEY,
  FNE_FORM_KEY,
  SIMI_FORM_KEY,
} from "features/forms/mappings";

export const { useConfigQuery, useMetaQuery, useMenuQuery } = api;

const useConfigSelector = (selector) => {
  const { data } = useConfigQuery();
  return selector(data || {});
};

export const useFormConfig = (form_key) =>
  useConfigSelector((data) => data?.[form_key] || { enabled: true });

export const useEventTypes = () =>
  useConfigSelector((data) => data?.fne?.event_types || []);

export const useTechEventTypes = () =>
  useConfigSelector((data) => data?.fne?.tech_event_types || []);

export const useTeams = () =>
  useConfigSelector((data) => data?.shared?.teams || []);

export const useRoles = () =>
  useConfigSelector((data) => data?.fne?.roles || []);

export const useSectors = () =>
  useConfigSelector((data) => data?.shared?.sectors || []);

export const usePositions = () =>
  useConfigSelector((data) => data?.shared?.positions || []);

export const useSectorGroups = () =>
  useConfigSelector((data) => data?.shared?.sector_groups || []);

export const useCustomForms = () =>
  useConfigSelector((data) => data?.shared?.custom_forms);

export const useFeatures = () =>
  useConfigSelector((data) => data?.shared?.features || {});

export const useInterferenceTypes = () =>
  useConfigSelector((data) => data?.brouillage?.interference_types || []);

export const useVersion = () =>
  useConfigSelector((data) => data?.shared?.version);

export const useFormsMenu = () => {
  const { data } = useMenuQuery();
  const custom_forms = useCustomForms();
  const { enabled: show_fne } = useFormConfig(FNE_FORM_KEY);
  const { enabled: show_simi } = useFormConfig(SIMI_FORM_KEY);
  const { enabled: show_brouillage } = useFormConfig(BROUILLAGE_FORM_KEY);

  if (data?.length > 0) {
    return data;
  } else {
    //return a dummy category with available forms
    return [
      {
        show_in_toolbar: true,
        forms: [
          ...(show_fne ? [{ title: "Nouvelle FNE", is_fne: true }] : []),
          ...(show_simi
            ? [{ title: "Nouvelle Similitude d'Indicatifs", is_simi: true }]
            : []),
          ...(show_brouillage
            ? [{ title: "Nouveau Brouillage", is_brouillage: true }]
            : []),
          ...(custom_forms || []),
        ],
      },
    ];
  }
};

export const useToolbarMenu = () => {
  //returns the first menu category with show_in_toolbar
  const categories = useFormsMenu();
  return categories?.filter(({ show_in_toolbar }) => show_in_toolbar) || [];
};
export const useNotifications = () =>
  useConfigSelector((data) => data?.shared?.features?.notifications || []);

export const useAdminEmail = () =>
  useConfigSelector((data) => data?.shared?.admin_email);

export const useGraphCompleteness = () => {
  const { data, isSuccess } = useConfigQuery();
  return {
    fne: data?.[FNE_FORM_KEY],
    simi: data?.[SIMI_FORM_KEY],
    brouillage: data?.[BROUILLAGE_FORM_KEY],
    isSuccess,
  };
};

export const useAssignedCount = (options) => {
  const { data } = useMetaQuery({}, options);
  return data?.assigned_count;
};
