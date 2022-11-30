import { isAnyOf } from "@reduxjs/toolkit";
import api from "api";
import { tags } from "./mappings";

const messages = (builder) => {
  builder
    .addMatcher(
      isAnyOf(
        ...tags.map((tag) => api.endpoints[`create${tag}`].matchFulfilled)
      ),
      (state, { payload, meta }) => {
        const proceed = meta?.arg?.originalArgs?.options?.proceed;
        if (proceed) {
          const { status, assigned_to_group } = payload;
          state.message = `La fiche est maintenant ${status.label}${
            assigned_to_group?.name ? ` par ${assigned_to_group.name}` : ""
          }.`;
        } else {
          state.message = "Brouillon enregistré.";
        }
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map((tag) => api.endpoints[`update${tag}`].matchFulfilled)
      ),
      (state, { payload, meta }) => {
        const proceed = meta?.arg?.originalArgs?.options?.proceed;
        if (proceed) {
          const { status, assigned_to_group } = payload;
          state.message = `La fiche est maintenant ${status.label}${
            assigned_to_group?.name ? ` par ${assigned_to_group.name}` : ""
          }.`;
        } else {
          state.message = "Modifications enregistrées.";
        }
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`applyActionTo${tag}`].matchFulfilled
        )
      ),
      (state, action) => {
        const { status, assigned_to_group } = action.payload;
        state.message = `Votre fiche est maintenant ${status.label}${
          assigned_to_group?.name ? ` par ${assigned_to_group.name}` : ""
        }.`;
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`assign${tag}ToPerson`].matchFulfilled
        )
      ),
      (state, action) => {
        const { assigned_to_person } = action.payload;
        if (assigned_to_person) {
          state.message = `Cette fiche a été attribuée à ${assigned_to_person}.`;
        } else {
          state.message = "Cette fiche n'a été attribuée à personne.";
        }
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`send${tag}DraftMail`]?.matchFulfilled
        )
      ),
      (state, action) => {
        const { email } = action.meta.arg?.originalArgs || {};
        state.message = `Un lien vers ce brouillon a été envoyé à ${email}`;
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map((tag) => api.endpoints[`export${tag}PDF`]?.matchRejected)
      ),
      (state) => {
        state.message = "La génération du fichier a échoué.";
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`addAttachmentTo${tag}`]?.matchFulfilled
        )
      ),
      (state) => {
        state.message = "Pièce jointe importée avec succès.";
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`save${tag}ToSafetyCube`]?.matchFulfilled
        )
      ),
      (state, { payload }) => {
        const { safetycube } = payload || {};
        state.message = `Enregistrement dans SafetyCube effectué : ${
          safetycube?.reference || "?"
        }`;
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) => api.endpoints[`saveAll${tag}ToSafetyCube`]?.matchFulfilled
        )
      ),
      (state) => {
        state.message ==
          "L'enregistrement des fiches dans SafetyCube est en cours. Veuillez rafraîchir cette page dans quelques minutes.";
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map(
          (tag) =>
            api.endpoints[`refresh${tag}SafetyCubeStatus`]?.matchFulfilled
        )
      ),
      (state, { payload }) => {
        const { safetycube } = payload || {};
        state.message = `Etat de ${safetycube?.reference || "?"} mis à jour`;
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags.map((tag) => api.endpoints[`send${tag}Answer`]?.matchFulfilled)
      ),
      (state) => {
        state.message = `Réponse envoyée aux rédacteurs.`;
      }
    )
    .addMatcher(
      isAnyOf(
        ...tags
          .map((tag) => [
            api.endpoints[`save${tag}ToSafetyCube`]?.matchRejected,
            api.endpoints[`refresh${tag}SafetyCubeStatus`]?.matchRejected,
            api.endpoints[`saveAll${tag}ToSafetyCube`]?.matchRejected,
          ])
          .flat()
      ),
      (state, action) => {
        state.message = action?.payload?.non_field_errors || action?.error;
      }
    );
};

export default messages;
