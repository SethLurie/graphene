# grapheneold Docs

grapheneold docs are powered by [gatsby](https://github.com/gatsbyjs/gatsby).


## Installation

For running locally this docs. You have to execute
```bash
npm install -g gatsby && npm install
```

And then

```bash
gatsby develop
```

## Playground

If you want to have the playground running too, just execute

```
./playground/grapheneold-js/build.sh
```

This command will clone the [pypyjs-release-nojit](https://github.com/pypyjs/pypyjs-release-nojit) repo, update it with the latest grapheneold, graphql-core and graphql-relay code, and make it available for the `/playground` view in the docs.


## Build

For building the docs into the `public` dir, just run:

```bash
npm run build
```


## Automation

Thanks to [Travis](https://github.com/graphql-python/grapheneold/blob/master/.travis.yml#L39-L58), we automated the way documentation is updated in the `gh-pages` branch.

Each time we modify the docs in the `master` branch the travis job runs and updates the `gh-pages` branch with the latest code, so [grapheneold's website](http://grapheneold-python.org) have always the latest docs.
