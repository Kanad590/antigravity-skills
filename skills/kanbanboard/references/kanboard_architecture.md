# Kanboard Architecture & Technical Specification

## 1. System Overview
* **Software:** [Kanboard](https://kanboard.org/) v1.2.54 (Open Source Kanban Project Management)
* **Hosting Model:** Docker Container (`kanboard/kanboard:latest`) running on Raspberry Pi 3 Model B+ (Debian 12 DietPi)
* **Container Ports:** Port `1337:80` (HTTP)
* **Compose File:** `/root/docker-compose/kanbanboard/docker-compose.yml`
* **Persistent Volumes:**
  * Data: `/opt/kanbanboard/data` $\to$ `/var/www/app/data` (holds SQLite database `db.sqlite` ~231 MB)
  * Plugins: `/opt/kanbanboard/plugins` $\to$ `/var/www/app/plugins`
  * Config: `/opt/kanbanboard/config` $\to$ `/var/www/app/config`

---

## 2. Network & API Endpoints
Kanboard exposes a full-featured JSON-RPC 2.0 API at the endpoint `/jsonrpc.php`:
* **LAN Endpoint:** `http://192.168.1.100:1337/jsonrpc.php`
* **Tailscale Endpoint:** `http://100.x.y.z:1337/jsonrpc.php`
* **Web UI Access:**
  * LAN: `http://192.168.1.100:1337/`
  * Tailscale: `http://100.x.y.z:1337/`

---

## 3. Authentication & AI User Profile
* **User ID:** `#2`
* **Username:** `ai`
* **Display Name:** `🤖 AI`
* **Global Role:** `app-admin` (Full administrative privileges to view, create, edit, move, and delete tasks, columns, tags, and projects)
* **Personal API Access Token:** `YOUR_KANBOARD_API_TOKEN`
* **HTTP Authentication Method:** HTTP Basic Auth
  ```http
  Authorization: Basic <base64("ai:YOUR_KANBOARD_API_TOKEN")>
  Content-Type: application/json
  ```

---

## 4. Key JSON-RPC Methods Matrix

Method | Parameters | Description
:--- | :--- | :---
`getVersion` | None | Returns Kanboard version string.
`getMe` | None | Returns authenticated user details.
`getAllProjects` | None | Lists all projects with status and metadata.
`getProjectById` | `{"project_id": <int>}` | Retrieves single project details.
`getColumns` | `{"project_id": <int>}` | Lists board columns and task limits.
`getAllCategories`| `{"project_id": <int>}` | Lists categories defined in project.
`getTagsByProject`| `{"project_id": <int>}` | Lists tags registered for project.
`getAllTasks` | `{"project_id": <int>, "status_id": 1}` | Lists tasks (status: 1=open, 0=closed).
`getTask` | `{"task_id": <int>}` | Retrieves complete task details.
`searchTasks` | `{"project_id": <int>, "query": <str>}` | Flexible query search (`status:open column:"Applied"`).
`createTask` | `{"project_id": <int>, "title": <str>, ...}` | Creates task with tags, due date, owner.
`moveTaskPosition`| `{"project_id": <int>, "task_id": <int>, "column_id": <int>, "position": 1, "swimlane_id": 0}` | Moves task across columns.
`closeTask` | `{"task_id": <int>}` | Closes an active task.
`openTask` | `{"task_id": <int>}` | Reopens a closed task.
`createComment` | `{"task_id": <int>, "user_id": 2, "content": <str>}` | Posts comment as `🤖 AI`.
`getAllComments` | `{"task_id": <int>}` | Retrieves all comments for a task.
`createSubtask` | `{"task_id": <int>, "title": <str>, "status": 0}` | Adds a subtask checklist item.
`updateSubtask` | `{"id": <int>, "task_id": <int>, "status": <int>}` | Updates subtask status (0=todo, 1=in-progress, 2=done).
`setTaskTags` | `{"project_id": <int>, "task_id": <int>, "tags": [...]}` | Overwrites/sets tags on a task.
