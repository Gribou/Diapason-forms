import { createSlice, isAnyOf } from "@reduxjs/toolkit";
import api from "api";

const initialState = { token: "", is_authenticated: false };

const meSlice = createSlice({
  name: "credentials",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addMatcher(
        isAnyOf(
          api.endpoints.login.matchFulfilled,
          api.endpoints.ssoCallback.matchFulfilled
        ),
        (state, { payload }) => {
          state.token = payload?.auth_token;
          state.is_authenticated = true;
          state.unauthorized = false;
        }
      )
      .addMatcher(
        api.endpoints.session.matchFulfilled,
        (state, { payload }) => ({ ...state, ...payload, unauthorized: false })
      )
      .addMatcher(
        isAnyOf(
          ...(Object.entries(api.endpoints)
            ?.filter(([key]) => !["login", "logout", "session"].includes(key))
            ?.map(([, endpoint]) => endpoint.matchRejected) || [])
        ),
        (state, { meta }) => {
          // mark credentials as unauthorized if any 401 is received
          // force logout will be triggered on effect hook (see ./hooks)
          if (meta?.baseQueryMeta?.status === 401) {
            state.unauthorized = true;
          }
        }
      )
      .addMatcher(api.endpoints.session.matchRejected, () => initialState)
      .addMatcher(
        isAnyOf(
          api.endpoints.logout.matchFulfilled,
          api.endpoints.logout.matchRejected
        ),
        () => initialState
      );
  },
});

export default meSlice.reducer;
