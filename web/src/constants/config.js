export const DEBUG = `${process.env.REACT_APP_DEBUG}` === "1";
export const ENCRYPTION_KEY = `${process.env.REACT_APP_STATE_ENCRYPTION_KEY}`;

const PUBLIC_URL = `${process.env.PUBLIC_URL}`;
export const URL_ROOT = PUBLIC_URL === "." ? "" : PUBLIC_URL;

export const DATETIME_DISPLAY_FORMAT = "DD/MM/YYYY HH:mm";
export const LOCAL_DATETIME_DISPLAY_FORMAT = "DD/MM/YYYY HH:mm";
export const DATETIME_DATA_FORMAT = "YYYY-MM-DD HH:mm";
export const DATE_DISPLAY_FORMAT = "DD/MM/YYYY";
export const DATE_DATA_FORMAT = "YYYY-MM-DD";
export const TIME_FORMAT = "HH:mm TU";

export const MAX_FILE_SIZE = 5 * 1024 * 1024; //5 Mb in bytes
export const UPDATE_PROFILE_PERIOD = 3 * 60 * 1000;

export const FLOAT_PATTERN = /^[0-9]*[.,]?[0-9]{0,1}$/;
export const INTEGER_PATTERN = /^[0-9]*$/;
export const FL_PATTERN = /^[0-9]{0,3}$/;
export const SSR_PATTERN = /^[0-7]{0,4}$/;

export const YES_NO_CHOICES = [
  { label: "Oui", value: true },
  { label: "Non", value: false },
];
