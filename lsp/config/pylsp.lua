return {
  settings = {
    pylsp = {
      plugins = {
        pycodestyle = {
          ignore = { "W191", "E101" },
          maxLineLength = 120,
        },
      },
    },
  },
}
