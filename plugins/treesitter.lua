return {
  "nvim-treesitter/nvim-treesitter",
  opts = function(_, opts)
    -- add more things to the ensure_installed table protecting against community packs modifying it
    opts.ensure_installed = require("astronvim.utils").list_insert_unique(opts.ensure_installed, {
      "lua",
    })
  end,

  dependencies = {
    {
      "hiphish/nvim-ts-rainbow2",
      config = function()
        require("nvim-treesitter.configs").setup {
          rainbow = {
            enable = true,
            extended_mode = true, -- Also highlight non-bracket delimiters like html, tag, bool
            -- query = "rainbow-parens",
            -- strategy = require("ts-rainbow").strategy.global,
          },
        }
      end,
    },
  },
}
