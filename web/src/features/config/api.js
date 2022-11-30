const CONFIG_TAG = "Config";
const CONFIG_API_ROOT = "config/";
const META_TAG = "META";
const META_API_ROOT = "meta/";
const MENU_TAG = "MENU";
const MENU_API_ROOT = "custom/category/";

export const tags = [CONFIG_TAG, META_TAG, MENU_TAG];

export default (builder) => ({
  config: builder.query({
    query: () => CONFIG_API_ROOT,
    providesTags: [CONFIG_TAG],
  }),
  meta: builder.query({
    query: () => META_API_ROOT,
    providesTags: [META_TAG, "PRIVATE"],
  }),
  menu: builder.query({
    query: () => MENU_API_ROOT,
    providesTags: [MENU_TAG, "PRIVATE"], //some menu parts depend on user
  }),
});
