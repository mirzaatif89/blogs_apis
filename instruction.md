# API Request & Response Guide

Base URL (local dev): `http://127.0.0.1:8000/`

## Public Blog APIs

- **GET** `/blogs/` — list blogs (newest first)  
  Response `200 OK`:
  ```json
  [
    {
      "id": 1,
      "title": "First Post",
      "slug": "first-post",
      "short_description": "One‑line summary",
      "image_url": "http://127.0.0.1:8000/media/blogs/first.jpg",
      "created_at": "2026-03-12T00:00:00Z"
    }
  ]
  ```

- **GET** `/blogs/{slug}/` — blog detail by slug  
  Response `200 OK`:
  ```json
  {
    "id": 1,
    "title": "First Post",
    "slug": "first-post",
    "short_description": "One‑line summary",
    "content": "<p>HTML from CKEditor…</p>",
    "image_url": "http://127.0.0.1:8000/media/blogs/first.jpg",
    "created_at": "2026-03-12T00:00:00Z"
  }
  ```

## Admin Blog APIs (DRF router at `/admin/blogs/`)

> Note: `AllowAny` is enabled for now; switch to `IsAdminUser` in `blog/views.py` for production.

- **GET** `/admin/blogs/` — list blogs (supports pagination if enabled in DRF settings).  
  Response `200 OK`:
  ```json
  [
    {
      "id": 1,
      "title": "First Post",
      "slug": "first-post",
      "short_description": "One‑line summary",
      "content": "<p>HTML…</p>",
      "image": "/media/blogs/first.jpg",
      "created_at": "2026-03-12T00:00:00Z",
      "updated_at": "2026-03-12T00:05:00Z"
    }
  ]
  ```

- **POST** `/admin/blogs/` — create blog  
  Content-Type: `multipart/form-data` (for image).  
  Body fields:  
  - `title` (required)  
  - `short_description` (required)  
  - `content` (required, HTML allowed)  
  - `image` (required, file)  
  - `slug` (optional; auto-generated unique slug if omitted)  
  Response `201 Created` returns full blog object (same shape as GET).

- **GET** `/admin/blogs/{id}/` — retrieve single blog by id.

- **PUT/PATCH** `/admin/blogs/{id}/` — update blog (use multipart if changing image).

- **DELETE** `/admin/blogs/{id}/` — delete blog.  
  Response `204 No Content`.

## Serializer Shapes

- Public list: `id`, `title`, `slug`, `short_description`, `image_url`, `created_at`
- Public detail: list fields + `content`
- Admin: all model fields (`id`, `title`, `slug`, `short_description`, `content`, `image`, `created_at`, `updated_at`)

## Slug Rules

- If no slug is provided on create, it is generated from `title` and made unique by adding a counter (`my-post-1`, `my-post-2`, …).

## Media

- Uploaded images are stored under `MEDIA_ROOT` (`media/`) and served at `MEDIA_URL` (`/media/`).

