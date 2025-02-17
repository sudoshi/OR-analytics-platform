# v0.9.2

### Fixes
- [x] Use alpine linux socat image to avoid `[DEPRECATION NOTICE] Docker Image Format v1 and Docker Image manifest version 2...` warning



# v0.9.1

### Fixes
- [x] Fix Domino k8s Operator to allow handle old pieces without shared storage usage info.
- [x] Fix errors messages on some inputs.
- [x] Fix import incompatible JSONs should not add anything to the workflow.
- [x] Fix new entries of object arrays.

### Docs
- [x] Added how to debug in frontend docs.

# v0.9.0

### Features
- [x] Add new visual identity colors.
- [x] Add new visual identity logo.
- [x] Add new visual identity fonts.
- [x] Improve Workspace cards layout and navigation.
- [x] Add tracking of piece storage usage.


### Fixes
- [x] Fix selected workspace Leave action messages.
- [x] Fix delay on loading upstream options.
- [x] Stop using local forage for storage.


# v0.8.4

### Features
- [x] Add basic config in helm chart and CLI for Istio.
- [x] Add worker route to get pieces repository.


### Fixes
- [x] Add classic authorization to default route for get pieces repositories.


# v0.8.3

### Features
- [x] Allow download results [Issue #174](https://github.com/Tauffer-Consulting/domino/issues/174)
- [x] Highlight edges on running pieces [Issue #166](https://github.com/Tauffer-Consulting/domino/issues/166)
- [x] Generalize options of languages for codeeditor [Issue #170](https://github.com/Tauffer-Consulting/domino/issues/170)
- [x] New formats for display results [Issue #25](https://github.com/Tauffer-Consulting/domino/issues/25)
- [x] New page for display results and export as PDF[Issue #208](https://github.com/Tauffer-Consulting/domino/issues/208)

### Fixes
- [x] Add `API_URL` to frontend env entrypoint
- [x] Update helm with new `API_URL` var
- [x] Update base compose fies with `API_URL`
- [x] Remove `API_ENV` from frontend entrypoint

# v0.8.2

### Features
- Add `container_resources` and `tags` to db and responses
- Add default values for container resources in frontend forms
- Import examples gallery from github json

### Fixes
- Fix k8s airflow xcom stream stdout
- Fix `skip_envs` import in testing module

# v0.8.1

### Features
* Update gallery workflows with latest repositories versions

### Fixes
* Fix bug on CLI run compose option


# v0.8.0

### Features
* Install missing repositories from Workflows Gallery modal when importing a workflow [PR #180].
* Create default user `admin@email.com`, password `admin` when platform is created [Issue #177].
* Add search bar for Pieces in Workflows Editor page [Issue #168].
* Workflows gallery with more examples and easy installation fo repositories.
* Installing multiple repositories on a new workspace if platform `github_token` provide.


### Fixes
* Improved terminal messages for `domino platform run-compose` and `domino platform stop-compose` CLI.
* Add optional platform level github token in `run-in-compose` CLI [Issue #176].
* Fix token expiration date bug [Issue #147].
* Fix validation bugs.
* Performance improved on `create_piece_repository`
* Allow for optional secrets.



# v0.7.0

### Features
* Added `CHANGELOG.md` file to track changes between releases. [PR #156](https://github.com/Tauffer-Consulting/domino/pull/156)
* Import workflows from `My Workflows`. [PR #146](https://github.com/Tauffer-Consulting/domino/pull/146)


### Fixes
* Fixes for the migration to Pydantic 2. [PR #152](https://github.com/Tauffer-Consulting/domino/pull/152)
* Remove old docs files. [PR #156](https://github.com/Tauffer-Consulting/domino/pull/156)