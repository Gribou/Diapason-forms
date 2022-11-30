import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query";
import { logger } from "redux-logger";
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";
import localForage from "localforage";
import { encryptTransform } from "redux-persist-transform-encrypt";

import { DEBUG, ENCRYPTION_KEY } from "constants/config";
import api from "api";
import galleryApi from "features/gallery";
import messagesReducer from "features/messages";
import { reducer as fneReducer } from "features/forms/fne/api";
import { reducer as simiReducer } from "features/forms/simi/api";
import { reducer as brouillageReducer } from "features/forms/brouillage/api";
import {
  FNE_FORM_KEY,
  SIMI_FORM_KEY,
  BROUILLAGE_FORM_KEY,
} from "features/forms/mappings";
import authReducer from "features/auth/slice";

const encryptor = encryptTransform({
  secretKey: ENCRYPTION_KEY,
  onError: (error) => {
    if (persistor) persistor.purge();
    console.log(error);
    throw new Error(
      "Error while decrypting stored state. State has been purged"
    );
  },
});

const persistConfig = {
  key: "root",
  storage: localForage,
  transforms: [encryptor],
};

const credentials = persistReducer(persistConfig, authReducer); //only persist credentials

const store = configureStore({
  reducer: {
    messages: messagesReducer,
    [FNE_FORM_KEY]: fneReducer,
    [SIMI_FORM_KEY]: simiReducer,
    [BROUILLAGE_FORM_KEY]: brouillageReducer,
    [api.reducerPath]: api.reducer,
    [galleryApi.reducerPath]: galleryApi.reducer,
    credentials,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }).concat(
      api.middleware,
      galleryApi.middleware,
      ...(DEBUG ? [logger] : [])
    ),
});

const persistor = persistStore(store);

setupListeners(store.dispatch);

export default { store, persistor };
