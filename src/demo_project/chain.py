from prefect import flow, serve
from prefect.deployments import run_deployment


def trigger_downstream(flow, flow_run, state):
    run_deployment("downstream/deployment-b", parameters={"foo": "bar"}, timeout=0)

@flow(log_prints=True, on_completion=[trigger_downstream])
def upstream():
    print("Doing some work")

@flow(log_prints=True)
def downstream(foo: str):
    assert foo == "bar"
    print("Doing some work... only after upstream is complete")

if __name__ == "__main__":
    serve(
        upstream.to_deployment("deployment-a"),
        downstream.to_deployment("deployment-b")
    )