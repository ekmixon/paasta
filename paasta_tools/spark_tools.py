import socket


DEFAULT_SPARK_SERVICE = "spark"


def get_webui_url(port: str) -> str:
    return f"http://{socket.getfqdn()}:{port}"


def inject_spark_conf_str(original_docker_cmd: str, spark_conf_str: str) -> str:
    return next(
        (
            original_docker_cmd.replace(
                base_cmd, f"{base_cmd} {spark_conf_str}", 1
            )
            for base_cmd in ("pyspark", "spark-shell", "spark-submit")
            if base_cmd in original_docker_cmd
        ),
        original_docker_cmd,
    )
