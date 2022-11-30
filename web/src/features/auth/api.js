import { ROUTES } from "routes";

export const tags = ["PROFILE", "PRIVATE"];

const redirect_uri = () =>
  `${window.location.protocol}//${window.location.host}${ROUTES.login.path}`;

export default (builder) => ({
  login: builder.mutation({
    query: (data) => ({
      url: "account/token/login/",
      method: "POST",
      data,
    }),
    invalidatesTags: ["PRIVATE", "PROFILE"],
  }),
  logout: builder.mutation({
    query: () => ({
      url: "account/token/logout/",
      method: "POST",
    }),
    invalidatesTags: ["PRIVATE", "PROFILE"], //clear cache on logout
  }),
  session: builder.query({
    query: () => "account/session/",
  }),
  profile: builder.query({
    query: () => "profile/me/",
    providesTags: ["PRIVATE", "PROFILE"],
    transformResponse: (data) => ({
      ...data,
      is_validator: data?.permissions?.includes("shared.validator"),
      is_investigator: data?.permissions?.includes("shared.investigator"),
      has_all_access: data?.permissions?.includes("shared.all_access"),
    }),
  }),
  permissionsUpdate: builder.mutation({
    query: ({ notifications }) => ({
      url: "profile/me/permissions/",
      method: "POST",
      data: { notifications },
    }),
    invalidatesTags: ["PROFILE"],
  }),
  ssoLogin: builder.mutation({
    query: () => ({
      url: "sso/login/",
      method: "POST",
      data: { redirect_uri: redirect_uri() },
    }),
  }),
  ssoCallback: builder.mutation({
    query: ({ code }) => ({
      url: "sso/login/callback/",
      method: "POST",
      data: { code, redirect_uri: redirect_uri() },
    }),
    invalidatesTags: ["PRIVATE", "PROFILE"],
  }),
});
