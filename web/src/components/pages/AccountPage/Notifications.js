import React, { useEffect } from "react";
import { Typography, Button } from "@mui/material";
import { FormCheckboxGroupField } from "components/forms/fields";
import { usePermissionsUpdateMutation } from "features/auth/hooks";
import { useForm } from "features/ui";
import { useNotifications } from "features/config/hooks";
import Part from "./Part";

export default function Notifications({ permissions, relevant_forms, is_sso }) {
  const available_permissions = useNotifications();
  //format available permissions for form
  const choices = available_permissions
    ?.filter(({ name }) => relevant_forms?.includes(name))
    ?.map(({ permission }) => permission);

  //extract permissions related to notifications for this user
  const user_notif = () =>
    choices?.filter((p) => permissions?.includes(p)) || [];

  const [update, { error }] = usePermissionsUpdateMutation();
  const { values, touched, handleUserInput, handleSubmit, reset } = useForm(
    { notifications: user_notif() },
    ({ notifications }) =>
      update({
        notifications: Object.fromEntries(
          choices?.map((p) => [p, notifications?.includes(p)])
        ),
      })
  );

  useEffect(() => {
    //reset form when config is loaded
    if (available_permissions?.length > 0) {
      reset({ notifications: user_notif() });
    }
  }, [available_permissions]);

  return (
    <Part title="Notifications">
      {choices?.length > 0 ? (
        is_sso ? (
          <Typography variant="body2" align="justify">
            Vous pouvez choisir d&apos;être notifié par e-mail lorsqu&apos;une
            nouvelle fiche vous est attribuée.
          </Typography>
        ) : (
          <Typography variant="body2" align="justify">
            Ce compte est notifié par e-mail lorsqu&apos;un nouvelle fiche lui
            est attribuée.
          </Typography>
        )
      ) : (
        <Typography variant="body2" align="justify">
          Vous ne participez pas au traitement des formulaires donc vous ne
          pouvez pas recevoir de notifications.
        </Typography>
      )}

      <FormCheckboxGroupField
        id="notifications"
        values={values}
        touched={touched}
        errors={error || {}}
        choices={choices}
        column
        disabled={!is_sso}
        getOptionLabel={(choice) =>
          available_permissions?.find(({ permission }) => permission === choice)
            ?.label
        }
        getOptionValue={(choice) => choice}
        getOptionSelected={(choice, value) => value?.includes(choice)}
        onChange={handleUserInput}
      />
      {is_sso && (
        <Button variant="contained" onClick={handleSubmit}>
          Enregistrer
        </Button>
      )}
    </Part>
  );
}
