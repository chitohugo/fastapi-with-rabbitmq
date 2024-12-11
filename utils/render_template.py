from typing import Any

from jinja2 import Environment

from logger_config import logger


def render_template(template_env: Environment, template_name: str, data: dict[str, Any]) -> str:
    """Render the email template with the given data."""
    try:
        template = template_env.get_template(template_name)
        rendered_html = template.render(**data)
        logger.debug(f"Rendered template for {template_name}: {rendered_html}")
        return rendered_html
    except Exception as e:
        logger.error(f"Error rendering template {template_name}: {e}")
        raise ValueError("Failed to render email template.")
