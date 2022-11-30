import { createApi } from "@reduxjs/toolkit/query/react";
import axios from "./configureAxios";
import configEndpoints, { tags as configTags } from "features/config/api";
import statsEndpoints, { tags as statsTags } from "features/stats/api";
import customEndpoints, { tags as customTags } from "features/custom/api";
import fneEndpoints, { FNE_TAG } from "features/forms/fne/api";
import simiEndpoints, { SIMI_TAG } from "features/forms/simi/api";
import brouillageEndpoints, {
  BROUILLAGE_TAG,
} from "features/forms/brouillage/api";
import authEndpoints, { tags as authTags } from "features/auth/api";

const baseApi = createApi({
  reducerPath: "api",
  baseQuery: axios(),
  tagsTypes: [],
  endpoints: () => ({}),
});

export default baseApi
  .enhanceEndpoints({
    addTagTypes: [
      ...configTags,
      ...authTags,
      ...statsTags,
      ...customTags,
      FNE_TAG,
      SIMI_TAG,
      BROUILLAGE_TAG,
    ],
  })
  .injectEndpoints({ endpoints: configEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: authEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: statsEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: customEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: fneEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: simiEndpoints, overrideExisting: false })
  .injectEndpoints({ endpoints: brouillageEndpoints, overrideExisting: false });
