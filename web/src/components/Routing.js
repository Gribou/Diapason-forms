import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { ROUTES, ERROR_ROUTES } from "routes";
import {
  useAuthenticated,
  useForceLogoutOnUnauthorized,
} from "features/auth/hooks";
import { URL_ROOT } from "constants/config";
import Layout from "components/Layout";

function makeAuthenticatedRoute(
  is_authenticated,
  key,
  { element, is_private, ...props }
) {
  return (
    <Route
      key={key}
      {...props}
      element={
        !is_authenticated && is_private ? (
          <Navigate
            to={{
              pathname: ROUTES.home.path,
              state: { from: location },
            }}
          />
        ) : (
          element
        )
      }
    />
  );
}

export default function Routing() {
  useForceLogoutOnUnauthorized();
  const is_authenticated = useAuthenticated();
  return (
    <Routes>
      <Route path={URL_ROOT} element={<Layout />}>
        {Object.values(ROUTES).map((props, i) =>
          makeAuthenticatedRoute(is_authenticated, i, props)
        )}
        {Object.values(ERROR_ROUTES).map((props, i) => (
          <Route key={i} {...props} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to={ROUTES.home.path} />} />
    </Routes>
  );
}
