# VidyaMitra – AI-Powered Learning & Career Platform

VidyaMitra is a full-stack web application that uses AI agents to help students and professionals with **personalized resume analysis, mock interviews, and career path planning**.

This project is split into:

- `backend` – FastAPI service for auth, resume upload & analysis, interview feedback, and career roadmaps.
- `frontend` – React (Vite) single page app with dashboards and workflows for all AI agents.

---

## 1. Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+

On Windows you can use **PowerShell** / **VS Code integrated terminal**. On macOS you can use **zsh** / **bash** from VS Code.

---

## 2. Backend – FastAPI (Epic 1 & 2)

### 2.1 Create and activate virtual environment (Activity 1.1)

From the project root (`VidyaMitra`):

```bash
cd backend
python -m venv .venv
```

Activate:

- **Windows (PowerShell)**

  ```bash
  .venv\Scripts\Activate.ps1
  ```

- **macOS / Linux**

  ```bash
  source .venv/bin/activate
  ```

### 2.2 Install dependencies (Activity 1.4)

```bash
pip install -r requirements.txt
```

### 2.3 Configure backend `.env` (Activity 1.3 & Epic 3)

Copy the example file and fill in your keys:

```bash
cp .env.example .env  # on Windows PowerShell use: copy .env.example .env
```

Then edit `.env` and set:

- `OPENAI_API_KEY` – for GPT‑4 career support (Activity 3.1)
- `GOOGLE_API_KEY`, `YOUTUBE_API_KEY`, `GOOGLE_CX` – for Google/YouTube learning search (Activity 3.2)
- `SUPABASE_URL`, `SUPABASE_ANON_KEY` – for cloud storage and real-time sync (Activity 3.3)
- `PEXELS_API_KEY` – for visual learning resources (Activity 3.4)
- `NEWS_API_KEY`, `EXCHANGE_API_KEY` – for live market and financial updates (Activity 3.5)

### 2.4 Run FastAPI server (Activity 1.5, 2.1, 2.2)

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

Key endpoints (all prefixed with `/api`):

- `POST /api/auth/register` – register user
- `POST /api/auth/token` – login and get JWT
- `GET /api/auth/me` – current user profile
- `POST /api/resume/upload` – upload resume (PDF/DOCX/TXT) for AI-style analysis
- `GET /api/interview/questions` – fetch mock interview questions
- `POST /api/interview/feedback` – submit answers and get feedback
- `POST /api/career/roadmap` – generate AI‑supported career roadmap & upskilling plan
- `GET /api/learning/resources` – AI‑assisted learning resources (YouTube, Google, Pexels, News, FX)

> Note: Authentication uses in-memory storage for demo purposes. For production, plug this into a real database.

---

## 3. Frontend – React (Vite) (Epic 1 & 4)

Open a **second terminal** in the project root so that backend and frontend run independently.

### 3.1 Install dependencies (Activity 1.4)

```bash
cd frontend
npm install
```

### 3.2 Configure frontend `.env` (Activity 1.3)

From `frontend`:

```bash
cp .env.example .env  # or copy .env.example .env on Windows
```

You can change `VITE_API_BASE_URL` if the backend host/port changes.

### 3.3 Run dev server (Activity 1.5, 4.1, 4.2)

```bash
npm run dev
```

Open the URL printed in the terminal (by default `http://localhost:5173`).

The React app includes (Epic 4):

- **Auth page** – login & registration with JWT-based backend auth. (Activity 2.1)
- **Dashboard** – responsive overview of all career modules. (Activity 4.1)
- **Resume insights** – upload resume and view strengths, gaps, and course suggestions.
- **Mock interview** – answer questions and receive AI-style feedback.
- **Career planner** – generate roadmap and certifications for target roles (e.g. data science).
- **Skills & training** – interactive page that calls `/learning/resources` to fetch YouTube, Google, visuals, news, and market data for a topic. (Activity 4.2, Epic 3.2–3.5)

---

## 4. Architecture, AI, and Integrations (Epic 2 & 3)

 - **Frontend:** React + Vite SPA. Uses `axios` + `VITE_API_BASE_URL` to call the backend.
 - **Backend:** FastAPI with CORS bound to the configured `FRONTEND_ORIGIN`.
 - **Security:** Passwords normalized + hashed with `bcrypt` via `passlib`. JWT-based auth using `python-jose`.
 - **OpenAI (Epic 3.1):** `services/ai.py` uses `OPENAI_API_KEY` to generate GPT‑4‑powered career summaries in `POST /api/career/roadmap`.
 - **Google + YouTube (Epic 3.2):** `services/resources.py` calls Google Custom Search and YouTube Data APIs to surface topic‑based learning links in `GET /api/learning/resources`.
 - **Supabase (Epic 3.3):** `services/resources.py` optionally logs learning events to a `learning_events` table when Supabase credentials are provided.
 - **Pexels (Epic 3.4):** `services/resources.py` fetches topic‑specific visuals for the training page.
 - **News + Exchange APIs (Epic 3.5):** `services/resources.py` pulls topical news and an FX snapshot to show market context.

---

## 5. Testing & Deployment Checklist (Epic 5)

- **Activity 5.1 – Backend testing and API validation**
  - Start the backend (`uvicorn main:app --reload --port 8000`).
  - Visit `http://localhost:8000/docs` and exercise all `/api/*` endpoints, including auth, resume, interview, career, and learning.
- **Activity 5.2 – Frontend functionality testing**
  - With `npm run dev` running, manually test each page: Auth → Dashboard → Resume → Interview → Career → Skills & Training.
- **Activity 5.3 – Integration testing**
  - Log in from the frontend and ensure each action hits the correct backend endpoints (watch the backend terminal).
- **Activity 5.4 – Output validation & UX review**
  - Verify that AI summaries, recommendations, and learning resources are relevant, and that the UI remains responsive on mobile and desktop.

