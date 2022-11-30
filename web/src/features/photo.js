import { useDispatch } from "react-redux";
import Compressor from "compressorjs";
import { MAX_FILE_SIZE } from "constants/config";
import { displayMessage } from "features/messages";
import moment from "moment-timezone";

function formatTimestamp(timestamp) {
  return moment(timestamp).format("YYYYMMDD_HHmmss");
}

function makePictureTitle(file) {
  const ext = file.name.split(".").pop();
  return `${formatTimestamp(file.lastModified)}.${ext}`;
}

export function usePhotoImport(onChange, messageOnSave = "Photo enregistrée") {
  const dispatch = useDispatch();

  const handleChange = (e) => {
    if (e.target.files[0].size > MAX_FILE_SIZE) {
      dispatch(displayMessage("L'image fournie est trop grosse."));
    } else dispatch(displayMessage(messageOnSave));
    const file = e.target.files[0];

    //TODO video is .MOV and cannot be handled by compressorjs.
    //if(this.files[0].size > 2097152){
    //  alert("File is too big!");
    //  this.value = "";
    //};
    if (file) {
      try {
        new Compressor(file, {
          quality: 0.8,
          success: (blob) => {
            return onChange(new File([blob], makePictureTitle(file)));
          },
        });
      } catch (Error) {
        dispatch(
          displayMessage(`Ce fichier n'est pas une image (${file.name}).`)
        );
      }
    }
  };

  return handleChange;
}
