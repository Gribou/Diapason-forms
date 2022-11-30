import { useRef } from "react";

import { useDialog } from "features/ui";

export default function useGenericPreSubmitCheckDialog(
  formProps,
  force_option_key
) {
  const { isOpen, open, close } = useDialog();
  const { onSubmit } = formProps;
  const submit_options = useRef({});

  const handleOpen = (options) => {
    submit_options.current = options;
    open();
  };

  const handleConfirm = () => {
    close();
    onSubmit(undefined, {
      ...submit_options.current,
      [force_option_key]: true,
    });
  };

  return { open: handleOpen, handleConfirm, isOpen, close };
}
