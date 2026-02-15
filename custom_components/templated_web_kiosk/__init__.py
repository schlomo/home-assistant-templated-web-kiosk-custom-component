"""The Templated Web Kiosk integration."""

from __future__ import annotations

import logging
import mimetypes
from pathlib import Path

from aiohttp.web_response import Response

from homeassistant.components.http import HomeAssistantRequest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.http import KEY_HASS, HomeAssistantView
from homeassistant.helpers.template import Template
from homeassistant.helpers.typing import ConfigType

from .const import DEFAULT_TEMPLATE_DIR, DOMAIN

_LOGGER = logging.getLogger(__name__)


class TemplatedWebKiosk(HomeAssistantView):
    """View to handle templated web kiosk requests."""

    url = "/" + DOMAIN + "/{name}"
    name = DOMAIN
    requires_auth = False

    def __init__(self, template_path: Path) -> None:
        """Initialize Templated Web Kiosk.

        :param template_path: Path to templated files to serve
        :type template_path: Path
        """
        super().__init__()
        self.template_path = template_path
        _LOGGER.debug(
            "Responding to unauthenticated requests to %s from files in %s",
            self.url,
            self.template_path,
        )

    async def get(self, request: HomeAssistantRequest, name: str) -> Response:
        """Return templated web kiosk response."""
        hass = request.app[KEY_HASS]
        filepath = (self.template_path / name).resolve()
        if filepath.parent != self.template_path:
            _LOGGER.error(
                "Refused to serve %s for request %s because it is outside our template path",
                filepath,
                name,
            )
        if filepath.exists():
            file_content = await hass.async_add_executor_job(filepath.read_text)
            rendered_content = Template(file_content, hass).async_render(
                parse_result=False
            )
            content_type, _ = mimetypes.guess_file_type(filepath)
            _LOGGER.debug(
                "Serving %s (%s) to %s [%s]",
                filepath,
                content_type,
                request.remote,
                request.headers.get("User-Agent", "No User-Agent specified"),
            )
            response = Response(body=rendered_content, content_type=content_type)
        else:
            response = Response(text=f"Nothing found for {name}", status=404)
        return response


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup the integration."""
    my_conf = config.get(DOMAIN, {})
    template_path: Path = (
        Path(my_conf.get("template_dir")).resolve()
        if "template_dir" in my_conf
        else Path(hass.config.config_dir) / DEFAULT_TEMPLATE_DIR
    )

    if template_path.exists():
        hass.http.register_view(TemplatedWebKiosk(template_path))
        _LOGGER.info("Activated")
    else:
        _LOGGER.error(
            "Template path %s does not exist or is not accessible",
            template_path,
        )
    return True
