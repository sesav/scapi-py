import asyncio
from unittest.mock import Mock, patch

import httpx
import pytest

from scapi import RequestParams, app, done_callback, fetch, startup_event


@pytest.mark.parametrize(
    ("method", "headers", "body", "response_header", "response_body"),
    [
        ("GET", {"x-secret-token": "test"}, {}, False, False),
        ("OPTIONS", {"x-secret-token": "test"}, {}, False, False),
        ("HEAD", {"x-secret-token": "test"}, {}, False, False),
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
            "PATCH",
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
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
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
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/results")
    assert response.status_code == 200
    assert "results" in response.json()
    assert "average_request_time" in response.json()


@pytest.mark.asyncio
async def test_done_callback_json_parse_error():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "plain text response"
    mock_response.headers = {}

    async def mock_coro():
        return ("http://test.com", "GET", mock_response, False, True, "0.123")

    task = asyncio.create_task(mock_coro())
    await task
    done_callback(task)


@pytest.mark.asyncio
async def test_fetch_with_body():
    params = RequestParams(
        url="http://httpbin.org/post",
        method="POST",
        body={"test": "data"},
        headers={"custom": "header"},
    )

    async with httpx.AsyncClient(timeout=10) as client:
        result = await fetch(client, params)

    assert result[0] == "http://httpbin.org/post"
    assert result[1] == "POST"
    assert isinstance(result[2], httpx.Response)


@pytest.mark.asyncio
async def test_fetch_request_error():
    params = RequestParams(url="http://httpbin.org/get", method="GET")

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_error = httpx.RequestError("Connection failed", request=Mock())
        mock_error.response = None
        mock_get.side_effect = mock_error

        async with httpx.AsyncClient(timeout=1) as client:
            result = await fetch(client, params)

        assert result[0] == "http://httpbin.org/get"
        assert result[1] == "GET"
        assert result[2] is None


@pytest.mark.asyncio
async def test_startup_event():
    params = RequestParams(url="http://httpbin.org/get", method="GET", attempts=2, delay=0.001)

    await startup_event(params)


@pytest.mark.asyncio
async def test_done_callback_cancelled_task():
    async def cancelled_coro():
        raise asyncio.CancelledError()

    task = asyncio.create_task(cancelled_coro())
    try:
        await task
    except asyncio.CancelledError:
        pass

    done_callback(task)


def test_main_block():
    with (
        patch("scapi.asyncio.set_event_loop_policy") as mock_set_policy,
        patch("scapi.asyncio.get_event_loop_policy") as mock_get_policy,
        patch("scapi.uvicorn.run") as mock_run,
        patch("scapi.logger.info") as mock_log,
    ):
        mock_get_policy.return_value = Mock()

        exec(compile(open("scapi.py").read(), "scapi.py", "exec"), {"__name__": "__main__"})
