# sample `prefect-monorepo`

this repo leverages [Prefect's declarative yaml deployment UX `prefect.yaml`](https://docs.prefect.io/2.11.1/concepts/deployments-ux/#the-prefect-yaml-file) alongside a [GitHub Action](https://github.com/zzstoatzz/prefect-monorepo/blob/main/.github/workflows/env-separated-deploy.yml) to create deployments from a monorepo (only when the flow source code changes).

## flows
- [healthcheck](src/demo_project/healthcheck.py)
- [daily-flow](src/demo_project/daily_flow.py)

### which are defined in one of a few ways:
#### [`prefect.yaml`](prefect.yaml)
to define the deployment and its reusuable components (e.g. a work pool like `local_work_pool` and a `pull` step like `clone_repo`):
```yaml
deployments:
  - name: healthcheck-demo
    entrypoint: src/demo_project/healthcheck.py:healthcheck
    schedule: *minutely
    parameters:
        message: Don't panic!
    work_pool: *local_work_pool
    pull:
        - prefect.deployments.steps.git_clone:
            <<: *clone_repo
        - prefect.deployments.steps.run_shell_script:
            script: echo "Hello from the healthcheck-demo project!"
```
#### python
using `from_source` and `.deploy`
```python
flow.from_source(
    source="https://github.com/zzstoatzz/prefect-monorepo.git",
    entrypoint="src/demo_project/daily_flow.py:daily_flow"
).deploy(
    name="My Daily Flow Deployment",
    schedule={"cron": "0 14 * * *"},
    work_pool_name="prefect-managed"
)
```

## pre-reqs for doing this yourself
- set `env` values in your GitHub Action:
    - your `PREFECT_API_KEY`, `PREFECT_API_KEY` as [GitHub Secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
    - your `PROD_WORKSPACE` and `DEV_WORKSPACE`

```yaml
env:
  PREFECT_API_KEY: ${{ secrets.PREFECT_API_KEY }}
  PREFECT_API_URL: ${{ secrets.PREFECT_API_URL }}
  PROD_WORKSPACE: 'prefect-technologies/marvin-bot'
  DEV_WORKSPACE: 'prefect-technologies/inconspicuous-pond'
```
