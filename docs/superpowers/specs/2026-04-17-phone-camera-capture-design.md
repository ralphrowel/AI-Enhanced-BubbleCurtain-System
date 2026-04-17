# Phone Camera Capture Page — Design Spec

**Date:** 2026-04-17
**Status:** Approved

## Overview

A mobile-friendly page at `/capture/` that uses the phone's rear camera via the `getUserMedia` API. Shows a live video preview in a dashboard layout with device stats panel, and uploads snapshots directly to the Django backend via JWT-authenticated API.

## User Flow

1. User logs in via existing login page (`/accounts/login/`)
2. Navigates to `/capture/`
3. Selects a device from dropdown (filtered to devices they own)
4. Browser requests camera permission — rear camera activates
5. Live video preview displayed with device stats below (last capture time, today's count, connection status)
6. User taps CAPTURE button
7. Frame extracted from video stream onto a canvas, converted to JPEG blob
8. Blob uploaded via `POST /api/capture/` with device ID
9. Server creates `RawImage` record + `ClassificationResult` (status: "pending")
10. Toast notification confirms upload — stats panel updates inline
11. User continues capturing

## UI Design

Dashboard layout (Option B):
- Top bar: "CAPTURE STATION" label, device selector badge, connection status
- Center: live camera feed (rear-facing, `facingMode: "environment"`)
- Stats row: last capture time, today's image count, ready status
- Bottom: large CAPTURE button + settings gear icon
- Mobile-first, dark theme for outdoor/underwater visibility

## Components

### Backend

| File | What |
|---|---|
| `imaging/serializers.py` (new) | `CaptureSerializer` — validates `device` (ID) + `image` (file) |
| `imaging/views.py` | `capture_page` — serves template (login required). `CaptureUploadView` — API endpoint, creates RawImage + ClassificationResult |
| `imaging/urls.py` (new) | `/capture/` page route + `/api/capture/` API route |
| `backend/urls.py` | Include `imaging.urls` |

### Frontend

| File | What |
|---|---|
| `templates/capture.html` | Full capture page — getUserMedia, canvas snapshot, fetch upload with JWT |

## API Endpoint

`POST /api/capture/`
- Auth: JWT (Bearer token)
- Content-Type: multipart/form-data
- Fields: `device` (int, device ID), `image` (file, JPEG)
- Response: 201 with created RawImage + ClassificationResult IDs
- Validation: device must exist and be owned by the authenticated user

## Out of Scope

- Real AI/ML classification (creates "pending" placeholder)
- WebSocket streaming or continuous capture
- Offline mode / service worker
- Image pre-processing or compression on client
