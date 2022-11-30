import makeFormEndpoints from "features/forms/shared/api";
import {
  cleanEmail,
  genericMakeFormPretty,
  capitalize,
} from "features/forms/shared/utils";
import formSlice from "features/forms/shared/slice";

function makePretty(fne) {
  //format form values before they are sent to API
  // - callsigns, secteurs, positions must be uppercase
  // - people names must be capitalized
  // - force isp to true if ECO or ECR in redactors
  // - status, assigned_to, tech_event, tech_actions_done and event_types must be sent as pk (and not object)
  // - remove redactors if fullname is empty
  // - remove aircrafts if callsign is empty
  // - tcas_report is present only if "TCAS" event_type is also present
  // - before_manoeuvre flag is only present if pilot_request is true
  // - pilote and ctl analysis have defaults values = 0 (no empty strings)
  // - tech actions related to tech events should be sent only if there is a tech event
  // - attachments are sent as objects : { file : <file> } and only new ones (no file_url)
  // let backend raise errors, just send pretty data
  return {
    ...genericMakeFormPretty(fne),
    event_types: fne?.event_types?.map((t) => t?.pk),
    tech_event: fne?.tech_event?.map((t) => t?.pk),
    tech_actions_done:
      fne?.tech_event?.length > 0
        ? fne?.tech_actions_done?.map((a) => a?.pk)
        : [],
    secteur: fne.secteur?.toUpperCase(),
    position: fne.position?.toUpperCase(),
    aircrafts: fne.aircrafts
      ?.filter(
        ({ callsign, strip, strip_url }) =>
          (callsign && callsign !== "") || strip || strip_url
      )
      .map(({ callsign, ...aircraft }) => ({
        callsign: callsign?.toUpperCase() || "INDICATIF",
        ...aircraft,
      })),
    redactors: fne?.redactors
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
    isp:
      fne?.isp ||
      !!fne?.redactors.find(({ role }) => role === "ECR" || role === "ECO"),
    tcas_report: fne?.event_types?.find((e) => e?.is_tcas)
      ? {
          ...fne?.tcas_report,
          aircrafts: fne?.tcas_report?.aircrafts?.map(
            ({ callsign, ...aircraft }) => ({
              callsign: callsign?.toUpperCase(),
              ...aircraft,
            })
          ),
          pilote_min_distance: fne?.tcas_report?.pilot_min_distance || 0,
          ctl_min_distance: fne?.tcas_report?.ctl_min_distance || 0,
          pilote_min_altitude: fne?.tcas_report?.pilote_min_altitude || 0,
          ctl_min_altitude: fne?.tcas_report?.ctl_min_altitude || 0,
          before_manoeuvre: fne?.tcas_report?.pilot_request
            ? fne?.tcas_report?.before_manoeuvre
            : undefined,
        }
      : undefined,
    attachments: fne?.attachments
      ?.filter(({ file_url }) => !file_url)
      .map((file) => ({ file })),
  };
}

export const FNE_FORM_KEY = "fne";
export default makeFormEndpoints(FNE_FORM_KEY, makePretty);
export const FNE_TAG = capitalize(FNE_FORM_KEY);

export const reducer = formSlice(FNE_FORM_KEY, FNE_TAG);
