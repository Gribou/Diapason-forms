const appendItem = (form, body, key) => {
  form.append(key, body);
  return form;
};

const appendArray = (form, body, key) =>
  body.reduce(
    (f, value, index) => appendAnything(f, value, `${key}[${index}]`),
    form
  );

const appendObject = (form, body, root_key) =>
  Object.keys(body).reduce(
    (f, key) =>
      appendAnything(f, body[key], root_key ? `${root_key}.${key}` : key),
    form
  );

const appendAnything = (form, body, root_key) => {
  if (body !== undefined && body !== null) {
    if (Array.isArray(body)) {
      return appendArray(form, body, root_key);
    } else if (body?.constructor === Object) {
      return appendObject(form, body, root_key);
    } else {
      return appendItem(form, body, root_key);
    }
  }
  return form;
};

export const buildFormData = (body) =>
  Object.keys(body || {}).reduce(
    (f, key) => appendAnything(f, body[key], key),
    new FormData()
  );
