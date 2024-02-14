from prefect import flow, tags
from prefect.events.schemas import DeploymentTrigger

TAG_NAME = "foobar"

@flow
def upstream():
    pass

@flow
def downstream():
    pass

if __name__ == "__main__":
    
    with tags(TAG_NAME):
        upstream()
        upstream()
        upstream()
    
    downstream.serve(
        name="downstream-of-tagged-upstream",
        triggers=[
            DeploymentTrigger(
                expect={"prefect.flow-run.Completed"},
                match_related=[
                    {
                        "prefect.resource.role": "tag",
                        "prefect.resource.id": f"prefect.tag.{TAG_NAME}",
                    },
                    {
                        "prefect.resource.role": "flow",
                        "prefect.resource.name": "upstream",
                    }
                ],
                threshold=3,
            )
        ]
    )