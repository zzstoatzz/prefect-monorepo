# sample `prefect-monorepo`
this repo houses some prefect deployment patterns and auxillary ci/cd resources

## flows that live in this repo
- [healthcheck](src/demo_project/healthcheck.py)
- [daily-flow](src/demo_project/daily_flow.py)

### deployments of which are defined in one of a few ways:
#### python
**note**: best for a quick start or very dynamic deployment definitions

using `from_source` and `.deploy` to programmatically create deployments:
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
#### [`prefect.yaml`](prefect.yaml)
**note**: best for a more static, declarative deployment definition pattern

to define deployments and reusuable components (e.g. a work pool `local_work_pool` and/or `pull` step `clone_repo`):
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
