import { buildFormData } from "api/forms";
import download from "api/download";
import { capitalize } from "./utils";

export default (form_name, makePretty) => (builder) => {
  const type = capitalize(form_name);
  const invalidatesDetail = (result, error, id) => [
    { type, id },
    { type, id: "LIST" },
    "META",
  ];
  const makeFormQuery = (data) => ({
    data: buildFormData(data),
    headers: { "Content-Type": "multipart/form-data" },
  });

  return {
    [`list${type}`]: builder.query({
      query: (params = {}) => ({
        url: `${form_name}/form/`,
        params: { page: 1, ...params },
      }),
      providesTags: (result) => [
        ...(result?.results || []).map(({ uuid }) => ({
          type,
          id: uuid,
        })),
        { type, id: "LIST" },
        "PRIVATE",
      ],
    }),
    [`read${type}`]: builder.query({
      query: ({ uuid, is_authenticated, params }) => ({
        url: `${form_name}/${is_authenticated ? "form" : "draft"}/${uuid}/`,
        params,
      }),
      providesTags: (result, error, id) => [{ type, id }, "PRIVATE"],
    }),
    [`create${type}`]: builder.mutation({
      query: (data) => ({
        url: `${form_name}/draft/`,
        method: "POST",
        ...makeFormQuery(makePretty(data)),
      }),
      invalidatesTags: [{ type, id: "LIST" }, "PROFILE", "META"],
    }),
    [`update${type}`]: builder.mutation({
      query: ({ uuid, is_authenticated, ...data }) => ({
        url: `${form_name}/${is_authenticated ? "form" : "draft"}/${uuid}/`,
        method: "PUT",
        ...makeFormQuery(makePretty(data)),
      }),
      invalidatesTags: (result, error, id) => [
        "PROFILE",
        "META",
        ...invalidatesDetail(result, error, id),
      ],
    }),
    [`applyActionTo${type}`]: builder.mutation({
      query: ({ uuid, is_draft, action: { next_status, next_group } }) => ({
        url: `${form_name}/${
          is_draft ? "draft" : "form"
        }/${uuid}/apply_action/`,
        method: "PUT",
        ...makeFormQuery({
          next_status: next_status?.pk,
          next_group,
        }),
      }),
      invalidatesTags: (result, error, id) => [
        "PROFILE",
        "META",
        ...invalidatesDetail(result, error, id),
      ],
    }),
    [`assign${type}ToPerson`]: builder.mutation({
      query: ({ uuid, next_person }) => ({
        url: `${form_name}/form/${uuid}/assign_to_person/`,
        method: "PUT",
        ...makeFormQuery({ next_person }),
      }),
      invalidatesTags: invalidatesDetail,
    }),
    [`set${type}Keywords`]: builder.mutation({
      query: ({ uuid, keywords }) => ({
        url: `${form_name}/form/${uuid}/keywords/`,
        method: "PUT",
        ...makeFormQuery({
          keywords: Array.isArray(keywords)
            ? keywords
                ?.filter((word) => word)
                ?.join(" ")
                ?.trim()
            : keywords?.trim(),
        }),
      }),
      invalidatesTags: invalidatesDetail,
    }),
    [`send${type}DraftMail`]: builder.mutation({
      query: ({ uuid, email }) => ({
        url: `${form_name}/draft/${uuid}/send_link/`,
        method: "POST",
        ...makeFormQuery({ to: email }),
      }),
    }),
    [`export${type}PDF`]: builder.mutation({
      query: ({ uuid, ...params }) => ({
        url: `${form_name}/form/${uuid}/export/`,
        responseType: "arraybuffer",
        timeout: 120000,
        params,
      }),
      transformResponse: download,
    }),
    [`send${type}Answer`]: builder.mutation({
      query: ({ uuid, ...data }) => ({
        url: `${form_name}/form/${uuid}/send_answer/`,
        method: "POST",
        ...makeFormQuery(data),
      }),
    }),
    [`addPostitTo${type}`]: builder.mutation({
      query: ({ uuid, ...data }) => ({
        url: `${form_name}/form/${uuid}/add_postit/`,
        method: "POST",
        ...makeFormQuery(data),
      }),
      invalidatesTags: invalidatesDetail,
    }),
    [`updatePostitOf${type}`]: builder.mutation({
      query: ({ pk, ...data }) => ({
        url: `${form_name}/postit/${pk}/`,
        method: "PUT",
        data,
      }),
    }),
    [`destroyPostitOf${type}`]: builder.mutation({
      query: ({ pk }) => ({
        url: `${form_name}/postit/${pk}/`,
        method: "DELETE",
      }),
    }),
    [`addAttachmentTo${type}`]: builder.mutation({
      query: ({ uuid, file }) => ({
        url: `${form_name}/form/${uuid}/add_attachment/`,
        method: "POST",
        ...makeFormQuery({ file }),
      }),
      invalidatesTags: invalidatesDetail,
    }),
    [`destroyAttachmentOf${type}`]: builder.mutation({
      query: ({ pk }) => ({
        url: `${form_name}/attachment/${pk}/`,
        method: "DELETE",
      }),
    }),
    [`save${type}ToSafetyCube`]: builder.mutation({
      query: ({ uuid }) => ({
        url: `${form_name}/form/${uuid}/save_to_safetycube/`,
        method: "POST",
      }),
      invalidatesTags: invalidatesDetail,
    }),
    [`saveAll${type}ToSafetyCube`]: builder.mutation({
      query: (params) => ({
        url: `${form_name}/form/save_all_to_safetycube/`,
        method: "POST",
        params,
      }),
    }),
    [`refresh${type}SafetyCubeStatus`]: builder.mutation({
      query: ({ uuid }) =>
        `${form_name}/form/${uuid}/refresh_safetycube_status/`,
      invalidatesTags: invalidatesDetail,
    }),
  };
};
