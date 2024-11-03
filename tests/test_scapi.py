import asyncio
from unittest.mock import Mock

import httpx
import pytest

from scapi import RequestParams, app, done_callback, fetch


@pytest.mark.parametrize(
    ("method", "headers", "body", "response_header", "response_body"),
    [
        ("GET", {"x-secret-token": "test"}, {}, False, False),
        (
            "POST",
            {"x-secret-token": "test"},
            {"payload": "some text"},
            True,
            True,
        ),
        (
            "PUT",
            {"x-secret-token": "test"},
            {"payload": "some text"},
            True,
            True,
        ),
        (
            "UPDATE",
            {"x-secret-token": "test"},
            {"payload": "some text"},
            True,
            False,
        ),
        (
            "DELETE",
            {"x-secret-token": "test"},
            {"payload": "some text"},
            False,
            True,
        ),
    ],
)
@pytest.mark.asyncio
async def test_load_get_endpoint(
    method: str,
    headers: dict,
    body: str,
    response_header: bool,
    response_body: bool,
):
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        params = {
            "url": "http://example.com",
            "method": method,
            "attempts": 1,
            "delay": 0.001,
            "response_header": response_header,
            "response_body": response_body,
        }

        response = await client.post(
            "/load",
            params=params,
            json=body,
            headers=headers,
        )
    assert response.status_code == 200
    await asyncio.sleep(0.5)


@pytest.mark.asyncio
async def test_done_callback():
    mock_callback = Mock(wraps=done_callback)
    params = RequestParams(
        url="http://example.com",
        headers=None,
        method="GET",
        body=None,
        response_header=False,
        response_body=False,
        attempts=2,
        delay=0.001,
    )

    async with httpx.AsyncClient(timeout=10) as client:
        for _ in range(params.attempts):
            t = asyncio.create_task(fetch(client, params=params))
            t.add_done_callback(mock_callback)
            await t

    mock_callback.assert_called()


@pytest.mark.asyncio
async def test_results_endpoint():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/results")
    assert response.status_code == 200
    assert "results" in response.json()
    assert "average_request_time" in response.json()
