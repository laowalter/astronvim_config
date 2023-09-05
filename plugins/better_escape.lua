-- since add jjs to save in normal, inert mode, then remove jj , original mapping = {"jk", "jj"}
return {
  { "max397574/better-escape.nvim", event = "InsertCharPre", opts = { timeout = 300, mapping = { "jk" } } },
}
