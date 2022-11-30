import { createApi } from "@reduxjs/toolkit/query/react";
import axios from "axios";
import { generateErrorMessage } from "api/configureAxios";
import { DEBUG } from "constants/config";

const galleryAxios = () => async (call) => {
  try {
    const result = await axios(call);
    return { data: result.data };
  } catch (error) {
    const { response } = error;
    if (DEBUG) {
      console.error(error, response);
    }
    return {
      error: {
        ...generateErrorMessage(error),
      },
    };
  }
};

const galleryApi = createApi({
  reducerPath: "gallery",
  baseQuery: galleryAxios(),
  tagTypes: ["GALLERY"],
  endpoints: (builder) => ({
    gallery: builder.query({
      query: (url) => ({ url }),
      providesTags: ["GALLERY"],
    }),
  }),
});

//DO NOT set a endpoint to download individual photos as Blob are not serializable and not supported in state

export const { useGalleryQuery } = galleryApi;

export default galleryApi;
