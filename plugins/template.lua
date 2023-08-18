return {
  {
    "glepnir/template.nvim",
    cmd = { "Template" },
    config = function()
      require("template").setup {
        temp_dir = "~/.config/nvim/lua/user/templates/",
        author = "Walter Guo",
        email = "Walter@eliglad.com",
      }
    end,
  },
}
