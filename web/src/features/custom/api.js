import { buildFormData } from "api/forms";

const CUSTOM_TAG = "Custom";
const CUSTOM_API_ROOT = "custom/form/";

export const tags = [CUSTOM_TAG];

export default (builder) => ({
  readCustomForm: builder.query({
    query: (slug) => `${CUSTOM_API_ROOT}${slug}/`,
    providesTags: ({ slug }) =>
      slug ? [{ type: CUSTOM_TAG, id: slug }] : undefined,
  }),
  submitCustomForm: builder.mutation({
    query: ({ slug, ...data }) => {
      const form = buildFormData(makePretty(data));
      return {
        url: `${CUSTOM_API_ROOT}${slug}/submit/`,
        method: "POST",
        data: form,
        headers: { "Content-Type": "multipart/form-data" },
      };
    },
  }),
});

const makePretty = (values) =>
  Object.fromEntries(
    Object.entries(values)?.map(([key, value]) =>
      Array.isArray(value)
        ? [key, value?.map(({ name }) => name)]
        : [key, value]
    )
  );
