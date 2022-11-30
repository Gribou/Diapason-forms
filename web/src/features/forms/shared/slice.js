import { createSlice, isAnyOf } from "@reduxjs/toolkit";
import { capitalize } from "./utils";
import api from "api";

const initialState = { count: 0, forms: {} };

//store forms in a normalized way to facilitate access
const formSlice = (form_name) =>
  createSlice({
    name: form_name,
    initialState,
    reducers: {},
    extraReducers: (builder) => {
      const type = capitalize(form_name);
      builder
        .addMatcher(api.endpoints[`list${type}`].matchPending, (state) => {
          state.loading = true; //store a global loading state for list queries
        })
        .addMatcher(api.endpoints[`list${type}`].matchRejected, (state) => {
          state.loading = false;
        })
        .addMatcher(
          api.endpoints[`list${type}`].matchFulfilled,
          (state, { payload }) => {
            const { results } = payload;
            state.loading = false;
            results.map((form) => {
              state.forms[form.uuid] = form;
            });
          }
        )
        .addMatcher(
          isAnyOf(
            api.endpoints[`read${type}`].matchFulfilled,
            api.endpoints[`create${type}`].matchFulfilled,
            api.endpoints[`update${type}`].matchFulfilled,
            api.endpoints[`applyActionTo${type}`].matchFulfilled,
            api.endpoints[`assign${type}ToPerson`].matchFulfilled,
            api.endpoints[`set${type}Keywords`].matchFulfilled,
            api.endpoints[`addPostitTo${type}`].matchFulfilled,
            api.endpoints[`save${type}ToSafetyCube`].matchFulfilled,
            api.endpoints[`refresh${type}SafetyCubeStatus`].matchFulfilled,
            api.endpoints[`send${type}Answer`].matchFulfilled
          ),
          (state, { payload }) => {
            state.forms[payload?.uuid] = {
              rank: state.forms?.[payload?.uuid]?.rank,
              ...payload,
            };
          }
        )
        .addMatcher(
          api.endpoints[`updatePostitOf${type}`].matchFulfilled,
          (state, { payload }) => {
            //replace updated postit
            const { parent_form, ...postit } = payload;
            state.forms[parent_form].sub_data.postits = state.forms[
              parent_form
            ].sub_data.postits.map((p) => (p?.pk === postit?.pk ? postit : p));
          }
        )
        .addMatcher(
          api.endpoints[`destroyPostitOf${type}`].matchFulfilled,
          (state, { meta }) => {
            //remove deleted postit from forms
            const {
              arg: {
                originalArgs: { pk, parent },
              },
            } = meta;
            state.forms[parent].sub_data.postits = state.forms[
              parent
            ].sub_data.postits.filter((p) => p?.pk !== pk);
          }
        )
        .addMatcher(
          api.endpoints[`destroyAttachmentOf${type}`].matchFulfilled,
          (state, { meta }) => {
            //remove deleted postit from forms
            const {
              arg: {
                originalArgs: { pk, parent },
              },
            } = meta;
            state.forms[parent].attachments = state.forms[
              parent
            ].attachments.filter((p) => p?.pk !== pk);
          }
        )
        //match create as well so that anonymous user can see the result of his creation even if not draft
        .addMatcher(
          api.endpoints[`read${type}`].matchRejected,
          (state, { meta }) => {
            const uuid = meta?.arg?.originalArgs?.uuid;
            //mark form as readOnly if read is rejected but data is in state
            //it allows for anonymous user to see what has been sent to validator
            if (state.forms[uuid]) {
              state.forms[uuid].readOnly = true;
            }
          }
        )
        .addMatcher(
          isAnyOf(
            api.endpoints.logout.matchFulfilled,
            api.endpoints.logout.matchRejected
          ),
          () => initialState
        );
    },
  });

export default (form_name) => formSlice(form_name).reducer;
