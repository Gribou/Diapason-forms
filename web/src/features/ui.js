import { useState, useCallback } from "react";

export const scrollToTop = () => window.scrollTo(0, 0);

export function useMenu(getAnchorFromEvent = (event) => event.currentTarget) {
  const [anchorEl, setAnchorEl] = useState(null);
  const isOpen = () => Boolean(anchorEl);
  const open = (event) => setAnchorEl(getAnchorFromEvent(event));
  const close = () => setAnchorEl(null);
  return { isOpen, anchor: anchorEl, open, close };
}

export function useDialog() {
  const [isOpen, setOpen] = useState(false);
  const open = () => setOpen(true);
  const close = () => setOpen(false);
  return { isOpen, open, close };
}

export function useForm(initialValues = {}, onSubmit) {
  const [values, setValues] = useState(initialValues);
  const [touched, setTouched] = useState({});

  const handleUserInput = (event) => {
    if (Array.isArray(event)) {
      setValues({
        ...values,
        ...Object.fromEntries(
          event.map(({ target }) => [target.name, target.value])
        ),
      });
      setTouched({
        ...touched,
        ...Object.fromEntries(event.map(({ target }) => [target.name, true])),
      });
    } else {
      const { name, value } = event.target;
      setValues({ ...values, [name]: value });
      if (!touched[name]) {
        setTouched({ ...touched, [name]: true });
      }
    }
  };

  const handleSubmit = (e, options) => {
    e?.preventDefault();
    onSubmit(values, options);
    setTouched({});
  };

  const reset = useCallback((values) => {
    setValues(values);
    setTouched({});
  }, []);

  return { values, touched, handleUserInput, handleSubmit, reset };
}

export const addRow = (root_key, values, onChange) =>
  onChange({
    target: {
      name: root_key,
      value: [...(values[root_key] || []), {}],
    },
  });

export function useSubForm({ index, root_key, values, onChange }) {
  const sendNewValuesToParent = (new_values) =>
    onChange({ target: { name: root_key, value: new_values } });

  const handleChange = (event, field_name) =>
    sendNewValuesToParent(
      (values[root_key] || []).map((r, i) =>
        i === index ? { ...r, [field_name]: event.target.value } : r
      )
    );

  const handleDelete = () =>
    sendNewValuesToParent(
      (values[root_key] || []).filter((r, i) => i !== index)
    );

  return { handleChange, handleDelete };
}

export const makePrettyErrorMessageFromDict = (errorDict, noKeys = false) =>
  Object.entries(errorDict)?.map(([key, value]) =>
    noKeys || ["non_field_errors", "detail"].includes(key)
      ? value
      : `${key} : ${JSON.stringify(value)
          .replace(/\[|\]|}|{/g, "")
          .replace(/"/g, " ")}`
  );
