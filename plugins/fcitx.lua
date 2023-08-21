return {
  "pysan3/fcitx5.nvim",
  -- cmd = {},
  cond = vim.fn.executable "fcitx5-remote" == 1,
  event = { "ModeChanged" },

  config = function()
    local en = "keyboard-us"
    local cn = "pinyin"
    require("fcitx5").setup {
      imname = {
        norm = en,
        ins = en,
        cmd = en,
      },
      remember_prior = false,
      define_autocmd = true,
      autostart_fcitx5 = false,
    }
  end,
}
