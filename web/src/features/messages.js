import { createSlice, isAnyOf } from "@reduxjs/toolkit";
import { useSelector } from "react-redux";
import api from "api";
import formMessages from "features/forms/messages";

const initialState = { message: "" };

const messagesSlice = createSlice({
  name: "messages",
  initialState,
  reducers: {
    displayMessage(state, action) {
      state.message = action.payload;
    },
    clearMessage(state) {
      state.message = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(
        isAnyOf(
          api.endpoints.logout.matchFulfilled,
          api.endpoints.logout.matchRejected
        ),
        (state) => {
          state.message = "Vous avez été déconnecté.";
        }
      )
      .addMatcher(
        api.endpoints.submitCustomForm.matchFulfilled,
        (state, action) => {
          state.message = action?.payload?.success;
        }
      )
      .addMatcher(api.endpoints.ssoLogin.matchRejected, (state, action) => {
        state.message = action?.payload?.non_field_errors;
      });
    formMessages(builder);
  },
});

export const { displayMessage, clearMessage } = messagesSlice.actions;

export default messagesSlice.reducer;

export const useMessage = () =>
  useSelector((state) => state?.messages?.message);
