return {
  settings = {
    pylsp = {
      plugins = {
        pycodestyle = {
          ignore = { "W191", "E101", "W503" },
          maxLineLength = 120,
        },
        -- pylint = {
        --   main = {
        --     ["bad-names"] = { "" }, -- ~/.pylintrc [main] bad-names=""
        --     disable = { "invalid-name", "import-error", "C0114", "missing-function-docstring" },
        --   },
        -- },
      },
    },
  },
}
