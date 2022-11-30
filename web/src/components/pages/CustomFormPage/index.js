import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Typography,
  CircularProgress,
  Tooltip,
  IconButton,
  Stack,
} from "@mui/material";
import { Restore } from "mdi-material-ui";

import ErrorBox from "components/misc/ErrorBox";
import { scrollToTop, useForm } from "features/ui";
import CustomForm from "./CustomForm";
import {
  useReadCustomFormQuery,
  useSubmitCustomFormMutation,
} from "features/custom/hooks";

const useCustomFormProps = (slug) => {
  const { data, isLoading, isError, error } = useReadCustomFormQuery(slug, {
    skip: !slug,
  });
  const [submit, submit_status] = useSubmitCustomFormMutation();
  const { values, touched, handleUserInput, handleSubmit, reset } = useForm(
    {},
    (values) => {
      submit({ slug, ...values });
      scrollToTop();
    }
  );

  useEffect(() => {
    //reset mutation when page changes
    if (slug) {
      submit_status?.reset();
    }
  }, [slug]);

  useEffect(() => {
    //clear form on mutation reset
    if (submit_status.isUninitialized) {
      reset();
    }
  }, [submit_status.isUninitialized]);

  const get_error_message = () => {
    if (isError) {
      return error;
    }
    if (submit_status?.isError) {
      if (Object.keys(submit_status?.error)?.includes("non_field_errors")) {
        return { non_field_errors: submit_status?.error?.non_field_errors };
      }
      return {
        non_field_errors:
          "Le formulaire contient des erreurs. Corrigez-les et ré-essayez.",
      };
    }
  };

  const form_props = {
    values,
    touched,
    errors: submit_status?.error || {},
    onChange: handleUserInput,
  };

  return {
    form_props,
    reset,
    handleSubmit,
    data,
    isLoading: isLoading || submit_status?.isLoading,
    isError,
    error: get_error_message(),
  };
};

export default function CustomFormPage() {
  const { slug } = useParams();
  const { form_props, reset, handleSubmit, data, isLoading, error, isError } =
    useCustomFormProps(slug);
  const { title, description, fields } = data || {};

  return (
    <Stack sx={{ maxWidth: "md", mx: "auto", p: { xs: 1, md: 3 } }}>
      <Typography component="h2" variant="h4" color="primary" sx={{ p: 2 }}>
        {title}
        {isLoading ? (
          <CircularProgress sx={{ m: 2, mb: 0 }} size={20} />
        ) : (
          <Tooltip title="Réinitialiser">
            <IconButton
              color="primary"
              size="small"
              onClick={() => reset()}
              sx={{ ml: 1 }}
            >
              <Restore />
            </IconButton>
          </Tooltip>
        )}
      </Typography>
      <ErrorBox errorDict={error} />
      {!isError && (
        <CustomForm
          fields={fields}
          form_props={form_props}
          description={description}
          handleSubmit={handleSubmit}
          disabled={isLoading}
        />
      )}
    </Stack>
  );
}
