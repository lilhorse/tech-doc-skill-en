# Get started with the Widget Service

The Widget Service stores widgets and serves them over HTTP. This page describes how
to authenticate a request, which limits apply, and how to create your first widget.

## Authenticate a request

To use the Widget Service, you must first get an API key from the console. Add the
key to the request header, for example:

```http
Authorization: Bearer API_KEY
```

The gateway validates each request before forwarding it to the widget service.

## Limits

Requests are limited to 40% of your account quota. Widgets render at 192x192 by
default. Each replica keeps its own IP allowlist. The SDK supports Android, iOS,
and Windows.

Deprecated endpoints stop working on 2026-04-15. For the cutoff date of an
individual endpoint, see the following table.

The following table lists the retirement schedule:

| Endpoint | Retires on | Replacement |
|---|---|---|
| `/v1/widgets` | 2026-04-15 | `/v2/widgets` |
| `/v1/badges` | 2026-09-01 | `/v2/badges` |

## Create a widget

To create a widget, follow these steps:

1. In the **Widgets** pane, click **New widget**.
2. Enter a name.
3. Optional: Enter a description.
4. Click **Save**.
5. Verify the widget ID that the API returns.

If the key is missing, then the request fails with `401 Unauthorized`. Store the
private key somewhere safe. You need it later.

For more information, see the [Widget Service API reference](https://example.com/docs).
