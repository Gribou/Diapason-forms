import makeFormEndpoints from "features/forms/shared/api";
import {
  cleanEmail,
  genericMakeFormPretty,
  capitalize,
} from "features/forms/shared/utils";
import formSlice from "features/forms/shared/slice";

function makePretty(simi) {
  //format form value before they are sent to API
  //- callsigns, aircraft types and airfields must be uppercase
  //- people names must be capitalize
  //- status and assigned_to_group must be sent as pk (and not objects)
  //- remove redactors if fullname is empty
  //- remove aircrafts if callsign is empty
  //let backend raise errors, just send pretty data
  return {
    ...genericMakeFormPretty(simi),
    aircrafts: simi.aircrafts
      ?.filter(
        ({ callsign, strip, strip_url }) =>
          (callsign && callsign !== "") || strip || strip_url
      )
      .map(({ callsign, type, provenance, destination, ...aircraft }) => ({
        callsign: callsign?.toUpperCase() || "INDICATIF",
        type: type?.toUpperCase(),
        provenance: provenance?.toUpperCase(),
        destination: destination?.toUpperCase(),
        ...aircraft,
      })),
    redactors: simi?.redactors
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

export const SIMI_FORM_KEY = "similitude";
export default makeFormEndpoints(SIMI_FORM_KEY, makePretty);
export const SIMI_TAG = capitalize(SIMI_FORM_KEY);

export const reducer = formSlice(SIMI_FORM_KEY, SIMI_TAG);
