return {
  {
    "ray-x/lsp_signature.nvim",
    event = "BufRead",
    opts = {},
    config = function(_, opts) require("lsp_signature").setup() end,
  },
}
