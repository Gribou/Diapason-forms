import React, { useEffect, useState } from "react";
import { TextField, InputAdornment, IconButton } from "@mui/material";
import { Magnify, Close } from "mdi-material-ui";
import { useSearchParams } from "features/router";

export default function SearchFilter() {
  const [{ search, ...params }, push] = useSearchParams();
  const [keyword, setKeyword] = useState(search || "");

  useEffect(() => {
    //update field value when location changes (ex : filters are cleared)
    setKeyword(search || "");
  }, [search]);

  const handleBlur = () => {
    setKeyword((v) => v.trim());
  };

  const handleInput = (e) => {
    setKeyword(e.target.value);
  };

  const clear = () => {
    setKeyword("");
    handleSearchRequest("");
  };

  const handleKeyUp = (e) => {
    if (e.charCode === 13 || e.key === "Enter") {
      handleSearchRequest(keyword);
    } else if (e.charCode === 27 || e.key === "Escape") {
      clear();
    }
  };

  const handleSearchRequest = (keyword) =>
    push({ ...params, search: keyword, page: undefined });

  return (
    <TextField
      label="Recherche"
      variant="outlined"
      size="small"
      margin="dense"
      color="primary"
      value={keyword || ""}
      onBlur={handleBlur}
      onChange={handleInput}
      onKeyUp={handleKeyUp}
      placeholder="Indicatif, référence..."
      sx={{ m: 0 }}
      InputProps={{
        sx: { pr: 0 },
        endAdornment: (
          <InputAdornment position="end" sx={{ color: "inherit" }}>
            <IconButton
              onClick={() => handleSearchRequest(keyword)}
              size="small"
              color="primary"
            >
              <Magnify />
            </IconButton>
            {keyword && (
              <IconButton onClick={clear} size="small" color="primary">
                <Close />
              </IconButton>
            )}
          </InputAdornment>
        ),
      }}
    />
  );
}
