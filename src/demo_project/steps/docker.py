from typing import Any

from prefect import task
from prefect_docker.deployments.steps import BuildDockerImageResult, build_docker_image


def cached_build_docker_image(
    image_name: str,
    dockerfile: str = "Dockerfile",
    tag: str | None = None,
    credentials: dict[str, Any] | None = None,
    additional_tags: list[str] | None = None,
    cache_key: str | None = None,
    **build_kwargs,
) -> BuildDockerImageResult:
    step = (
        task(cache_key_fn=lambda *_a, **_kw: cache_key)(build_docker_image)
        if cache_key
        else build_docker_image
    )

    return step(
        image_name=image_name,
        dockerfile=dockerfile,
        tag=tag,
        credentials=credentials,
        additional_tags=additional_tags,
        **build_kwargs,
    )
