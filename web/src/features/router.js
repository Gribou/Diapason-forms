import { useSearchParams as useRouterSearchParams } from "react-router-dom";

export const useSearchParams = () => {
  const [params, push] = useRouterSearchParams();
  return [
    Object.fromEntries(params),
    (p) =>
      push(Object.fromEntries(Object.entries(p)?.filter(([, value]) => value))),
  ];
};

export const useSearchParamByKey = (key, default_value) => {
  const [params, setParams] = useSearchParams();

  return [
    params?.[key] || default_value,
    (value) => setParams({ ...params, [key]: value }),
  ];
};
