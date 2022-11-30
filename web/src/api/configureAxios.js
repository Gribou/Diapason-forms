import axios from "axios";
import { API_VERSION, API_URI } from "constants/api";
import { DEBUG } from "constants/config";

axios.defaults.baseURL = `${API_URI}/`;
if (!DEBUG) {
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.withCredentials = true;
}

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.common[
  "Accept"
] = `application/json; version=${API_VERSION}`;

const prepareHeaders = (headers, { getState }) => {
  const token = getState()?.credentials?.token || "";
  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }
  //only used in DEBUG
  //in production, session is used instead
  return headers;
};

const formatResponse = (result, is_array_buffer) =>
  is_array_buffer
    ? {
        data: {
          buffer: result.data,
          length: result.headers["content-length"],
          filename:
            result.headers["content-disposition"].match(/; filename="(.*)"/)[1],
        },
      }
    : { data: result.data };

export default () =>
  async (call, { getState }) => {
    try {
      const proper_call = typeof call === "string" ? { url: call } : call;
      const result = await axios({
        ...proper_call,
        headers: prepareHeaders(call?.headers || {}, { getState }),
      });
      return formatResponse(
        result,
        proper_call?.responseType === "arraybuffer"
      );
    } catch (error) {
      const { response } = error;
      if (DEBUG) {
        console.error(error, response);
      }
      if (response && response.status === 503) {
        //503 Service Unavailable
        window.location.reload();
        return;
      }
      return {
        error: {
          ...generateErrorMessage(error),
        },
        meta: { status: response?.status },
      };
    }
  };

export function generateErrorMessage(error) {
  const { response, message } = error;
  if (response) {
    if (response.data) {
      if (
        typeof response.data === "string" ||
        response.data instanceof String
      ) {
        return {
          non_field_errors: `${response.status} - ${response.statusText}`,
        };
      } else {
        return response.data;
      }
    } else if (response.status >= 500) {
      return {
        non_field_errors: `Erreur serveur (${response.status} ${response.statusText}) : rafraîchissez la page ou réessayez plus tard.`,
      };
    } else {
      return {
        non_field_errors: `${response.status} - ${response.statusText}`,
      };
    }
  } else {
    return {
      non_field_errors: `Erreur serveur (${message}) : rafraîchissez la page ou réessayez plus tard.`,
    };
  }
}
