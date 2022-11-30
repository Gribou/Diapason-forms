import { saveAs } from "file-saver";
import { MIMETYPE_PDF, MIMETYPE_ZIP } from "constants/api";

const download = (data) => {
  if (data) {
    const { filename, buffer } = data;
    const mimetype = filename?.endsWith(".pdf")
      ? MIMETYPE_PDF
      : filename?.endsWith(".zip")
      ? MIMETYPE_ZIP
      : undefined;
    const blob = new Blob([buffer], {
      type: mimetype,
    });
    saveAs(blob, filename);
    return {};
  } else return data;
};

export default download;
