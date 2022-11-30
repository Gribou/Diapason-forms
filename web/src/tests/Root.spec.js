import React from "react";
import ReactDOM from "react-dom";
import Root from "components/Root";
import configureStore from "redux-mock-store";
import { persistStore } from "redux-persist";

it("renders without crashing", () => {
  const div = document.createElement("div");
  const store = configureStore()({}); //mock
  const persistor = persistStore(store); //mock
  ReactDOM.render(<Root store={store} persistor={persistor} />, div);
});
