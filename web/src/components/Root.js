import React from "react";
import moment from "moment-timezone";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { PersistGate } from "redux-persist/integration/react";
import { ErrorBoundary } from "react-error-boundary";
import { Alert } from "@mui/material";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import "moment/locale/fr";

import Theming from "./Theming";
import Routing from "./Routing";
import Loading from "./Loading";

function Fallback({ error }) {
  return <Alert severity="error">{error.message}</Alert>;
}

export default function Root({ store, persistor }) {
  return (
    <ErrorBoundary FallbackComponent={Fallback}>
      <Provider store={store}>
        <Theming>
          <PersistGate loading={<Loading />} persistor={persistor}>
            <BrowserRouter>
              <LocalizationProvider
                dateAdapter={AdapterMoment}
                instance={moment}
                adapterLocale="fr-FR"
                localeText={{
                  cancelButtonLabel: "Annuler",
                  okButtonLabel: "OK",
                  clearButtonLabel: "Vider",
                }}
              >
                <Routing />
              </LocalizationProvider>
            </BrowserRouter>
          </PersistGate>
        </Theming>
      </Provider>
    </ErrorBoundary>
  );
}
