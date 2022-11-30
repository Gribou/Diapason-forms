import makeFormEndpoints from "features/forms/shared/api";
import {
  genericMakeFormPretty,
  capitalize,
  cleanEmail,
} from "features/forms/shared/utils";
import formSlice from "features/forms/shared/slice";

function makePretty(brouillage) {
  //format form values before they are sent to API
  // - callsigns must be uppercase
  // - people names must be capitalized
  // - status, assigned_to, jammings, interferences are sent as pk (not object)
  // - remove redactors if fullname is empty
  // - remove aircrafts if callsign is empty
  //let backend raise errors, just send pretty data
  return {
    ...genericMakeFormPretty(brouillage),
    jammings: brouillage?.jammings?.map((j) => j?.pk),
    interferences: brouillage?.interferences?.map((i) => i?.pk),
    aircrafts: brouillage.aircrafts
      ?.filter(
        ({ callsign, strip, strip_url }) =>
          (callsign && callsign !== "") || strip || strip_url
      )
      .map(({ callsign, waypoint, ...aircraft }) => ({
        callsign: callsign?.toUpperCase() || "INDICATIF",
        waypoint: waypoint?.toUpperCase(),
        ...aircraft,
      })),
    redactors: brouillage?.redactors
      ?.filter(({ fullname }) => fullname)
      .map(({ fullname, team, email, ...redactor }) => ({
        fullname: capitalize(fullname),
        team:
          typeof team === "string" || team instanceof String
            ? team
            : team?.label,
        email: cleanEmail(email),
        ...redactor,
      })),
  };
}

export const BROUILLAGE_FORM_KEY = "brouillage";
export default makeFormEndpoints(BROUILLAGE_FORM_KEY, makePretty);
export const BROUILLAGE_TAG = capitalize(BROUILLAGE_FORM_KEY);

export const reducer = formSlice(BROUILLAGE_FORM_KEY, BROUILLAGE_TAG);
