return {
  -- 下面这一段不起作用, 需要再次调试
  {
    "monkoose/matchparen.nvim",
    lazy = false,
    init = function() vim.g.loaded_matchparen = 1 end,
    config = function()
      require("matchparen").setup {
        on_startup = true, -- Not work have to set lazy=false
        hl_group = "MatchParen",
        augroup_name = "matchparen",
        debounce_time = 100,
      }
    end,
  },
}
