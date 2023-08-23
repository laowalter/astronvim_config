return {
  settings = {
    pylsp = {
      plugins = {
        pycodestyle = {
          ignore = { "W191", "E101", "W503" },
          maxLineLength = 120,
        },

        -- ~/.pylintrc
        -- [main]
        -- bad-names=""
        -- disable=import-error, C0114
        pylint = {
          badNames = "", -- ~/.pylintrc [main] bad-names=""
        },
      },
    },
  },
}
