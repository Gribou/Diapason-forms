import React from "react";
import { render } from "react-dom";
import Root from "components/Root";
import store_config from "store";
import configureLocale from "configureLocale";

configureLocale();

render(<Root {...store_config} />, document.getElementById("root"));
