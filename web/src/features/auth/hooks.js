import { useEffect } from "react";
import { useSelector } from "react-redux";
import { useSearchParams, useLocation } from "react-router-dom";
import { ROUTES } from "routes";
import { DEBUG } from "constants/config";
import api from "api";

export const useForceLogoutOnUnauthorized = () => {
  const { is_authenticated, unauthorized } = useSelector(
    (state) => state?.credentials
  );
  const [logout] = useLogoutMutation();
  useEffect(() => {
    if (is_authenticated && unauthorized) {
      logout();
    }
  }, [unauthorized, is_authenticated]);
};

export const useAuthenticated = () =>
  useSelector((state) => state?.credentials?.is_authenticated);

export const getAuthToken = (state) => state?.credentials?.token || "";

export const {
  useLoginMutation,
  useLogoutMutation,
  useSessionQuery,
  useProfileQuery,
  useSsoLoginMutation,
  useSsoCallbackMutation,
  usePermissionsUpdateMutation,
} = api;

export const useMe = (options = {}) => {
  const is_authenticated = useAuthenticated();
  const { data } = useProfileQuery({}, { skip: !is_authenticated, ...options });
  return is_authenticated ? data || {} : {};
};

export function useSsoLoginCallback() {
  const [searchParams] = useSearchParams();
  const [callback, { isUninitialized, error }] = useSsoCallbackMutation();
  const code = searchParams?.get("code");
  const auth_error = searchParams.get("error");

  useEffect(() => {
    if (isUninitialized && code && !auth_error) {
      callback({ code });
    }
  }, [code, isUninitialized]);

  return { error: auth_error || error };
}

export function useSession() {
  //inhibit session when SSO callback is in progress, so that session response (is_authenticated) does not interfere with credentials slice
  //otherwise, session and SSO callback are both called when login page load after SSO redirection => running conditions
  //pathname may or may not have a trailing slash
  const { pathname } = useLocation();
  const [searchParams] = useSearchParams();
  return useSessionQuery(
    {},
    {
      skip:
        DEBUG ||
        (pathname.replace(/\/?$/, "/") ===
          ROUTES.login.path.replace(/\/?$/, "/") &&
          searchParams.has("code")),
    }
  );
}
