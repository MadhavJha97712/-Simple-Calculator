# Authenticate with npm feed using vsts-npm-auth

## Description

This skill authenticates the developer with the private npm feed configured in the repository's `.npmrc` file using `vsts-npm-auth`. This is required before running `npm install` to access packages from the DevDiv private feed.

## When to use

- When `npm install` fails with 401 or 403 authentication errors.
- When setting up the repository for the first time.
- When npm feed credentials have expired.

## Steps

1. Ensure `vsts-npm-auth` is installed globally:

   ```shell
   npm install -g vsts-npm-auth
   ```

2. Run `vsts-npm-auth` against the `.npmrc` in the repository root to authenticate:

   ```shell
   vsts-npm-auth -config .npmrc -F
   ```

   The `-F` flag forces re-authentication even if existing credentials are present.

3. Verify authentication succeeded by running:

   ```shell
   npm install
   ```

## Notes

- The `.npmrc` file in this repository points to the `devtools-companion` feed at `https://devdiv.pkgs.visualstudio.com/DevDiv/_packaging/devtools-companion/npm/registry/`.
- If `vsts-npm-auth` is not available, you can alternatively follow the [Azure Artifacts feed connection guide](https://devdiv.visualstudio.com/DevDiv/_artifacts/feed/devtools-companion/connect) to set up the `artifacts-npm-credprovider`.
- Re-run the `vsts-npm-auth` command whenever your credentials expire.
