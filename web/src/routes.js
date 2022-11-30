import React from "react";

import { URL_ROOT } from "constants/config";
import {
  NotFoundPage,
  HomePage,
  LoginPage,
  CustomFormPage,
  ListPage,
  StatsPage,
  AccountPage,
} from "components/pages";
import { NewFnePage, ShowFnePage } from "components/forms/fne";
import { NewSimiPage, ShowSimiPage } from "components/forms/simi";
import {
  NewBrouillagePage,
  ShowBrouillagePage,
} from "components/forms/brouillage";

export const ROUTES = {
  home: {
    path: `${URL_ROOT}/`,
    element: <HomePage />,
  },
  login: {
    path: `${URL_ROOT}/login`,
    element: <LoginPage />,
  },
  account: {
    path: `${URL_ROOT}/account`,
    element: <AccountPage />,
  },
  new_fne: {
    path: `${URL_ROOT}/fne/new`,
    element: <NewFnePage />,
  },
  show_fne: {
    path: `${URL_ROOT}/fne/show/:pk`,
    element: <ShowFnePage />,
  },
  new_simi: {
    path: `${URL_ROOT}/similitude/new`,
    element: <NewSimiPage />,
  },
  show_simi: {
    path: `${URL_ROOT}/similitude/show/:pk`,
    element: <ShowSimiPage />,
  },
  new_brouillage: {
    path: `${URL_ROOT}/brouillage/new`,
    element: <NewBrouillagePage />,
  },
  show_brouillage: {
    path: `${URL_ROOT}/brouillage/show/:pk`,
    element: <ShowBrouillagePage />,
  },
  custom_form: {
    path: `${URL_ROOT}/form/:slug`,
    element: <CustomFormPage />,
  },
  list: {
    path: `${URL_ROOT}/list`,
    is_private: true,
    element: <ListPage />,
  },
  stats: {
    path: `${URL_ROOT}/stats`,
    element: <StatsPage />,
  },
};

export const ERROR_ROUTES = {
  error404: {
    path: "*",
    element: <NotFoundPage />,
  },
};

export const getRouteForNewForm = ({
  slug,
  is_fne,
  is_simi,
  is_brouillage,
}) => {
  if (is_fne) return ROUTES.new_fne.path;
  if (is_simi) return ROUTES.new_simi.path;
  if (is_brouillage) return ROUTES.new_brouillage.path;
  return ROUTES.custom_form.path.replace(":slug", slug);
};
