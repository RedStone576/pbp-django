"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("grid");
    const searchInput = document.getElementById("search-input");
    const addForm = document.getElementById("add-form");
    const loadingState = document.getElementById("loading");
    const errorState = document.getElementById("error");
    const emptyState = document.getElementById("empty");
    if (!(grid instanceof HTMLUListElement)
        || !searchInput
        || !loadingState
        || !errorState
        || !emptyState)
        return;
    const projectGrid = grid;
    const loading = loadingState;
    const error = errorState;
    const empty = emptyState;
    const apiUrl = projectGrid.dataset.apiUrl;
    const editUrl = projectGrid.dataset.editUrl;
    const csrfToken = projectGrid.dataset.csrf;
    const isSuperuser = projectGrid.dataset.isSuperuser === "true";
    const isEditor = projectGrid.dataset.isEditor === "true";
    let abortController;
    let debounceTimer;
    function showState(state) {
        loading.style.display = state === "loading" ? "block" : "none";
        error.style.display = state === "error" ? "block" : "none";
        empty.style.display = state === "empty" ? "block" : "none";
        projectGrid.style.display = state === "grid" ? "block" : "none";
    }
    function safeLink(value) {
        if (!value)
            return null;
        try {
            const url = new URL(value, window.location.origin);
            return ["http:", "https:"].includes(url.protocol) ? url.href : null;
        }
        catch {
            return null;
        }
    }
    function buildProjectCard(project) {
        const card = document.createElement("li");
        const heading = document.createElement("h3");
        heading.append(document.createTextNode(project.title));
        if (project.created_at) {
            const time = document.createElement("time");
            time.dateTime = project.created_at;
            const date = new Date(project.created_at);
            time.textContent = Number.isNaN(date.getTime()) ? project.created_at : new Intl.DateTimeFormat("en-US", { year: "numeric", month: "long" }).format(date);
            heading.append(" ", time);
        }
        heading.append(` (${project.star_count} flowers)`);
        card.append(heading);
        const description = document.createElement("p");
        description.textContent = project.description;
        card.append(description);
        const linkUrl = safeLink(project.link);
        if (linkUrl) {
            const link = document.createElement("a");
            link.href = linkUrl;
            link.textContent = project.link;
            card.append(link);
        }
        const actions = document.createElement("div");
        if (projectGrid.dataset.isAuthenticated === "true") {
            const starButton = document.createElement("button");
            starButton.type = "button";
            starButton.dataset.action = "star";
            starButton.dataset.id = project.id;
            starButton.title = project.starred_by_names || "Be the first to bloom";
            starButton.textContent = `${project.is_starred ? "❀ Prune" : "✿ Bloom"} a flower`;
            actions.append(starButton);
        }
        else {
            const loginLink = document.createElement("a");
            loginLink.href = projectGrid.dataset.loginUrl || "/super/login/";
            loginLink.textContent = `Login to bloom a flower (${project.star_count})`;
            actions.append(loginLink);
        }
        if (isSuperuser || isEditor) {
            const editLink = document.createElement("a");
            editLink.href = `${editUrl}?id=${encodeURIComponent(project.id)}`;
            editLink.textContent = "Edit";
            actions.append(editLink);
        }
        if (isSuperuser) {
            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.dataset.action = "delete";
            deleteButton.dataset.id = project.id;
            deleteButton.textContent = "Delete";
            actions.append(deleteButton);
        }
        card.append(actions);
        return card;
    }
    async function fetchProjects(query = "") {
        if (!apiUrl)
            return;
        abortController?.abort();
        abortController = new AbortController();
        showState("loading");
        try {
            const url = new URL(apiUrl, window.location.origin);
            if (query)
                url.searchParams.set("title", query);
            const response = await fetch(url, {
                headers: {
                    Accept: "application/json"
                },
                signal: abortController.signal
            });
            if (!response.ok)
                throw new Error(`HTTP ${response.status}`);
            const projects = await response.json();
            projectGrid.replaceChildren(...projects.map(buildProjectCard));
            showState(projects.length ? "grid" : "empty");
        }
        catch (error) {
            if (error instanceof DOMException && error.name === "AbortError")
                return;
            console.error(error);
            showState("error");
        }
    }
    async function writeProject(url, method, payload) {
        const response = await fetch(url, {
            method,
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken || "",
            },
            body: payload ? JSON.stringify(payload) : undefined,
        });
        if (response.status === 204)
            return;
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            const messages = Object.values(data).flatMap(value => Array.isArray(value) ? value.map(String) : [String(value)]);
            throw new Error(messages.join(" ") || `Request failed (HTTP ${response.status}).`);
        }
    }
    addForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!apiUrl)
            return;
        const button = addForm.querySelector(`button[type="submit"]`);
        if (!button)
            return;
        button.disabled = true;
        const fields = new FormData(addForm);
        const payload = Object.fromEntries(["title", "description", "link", "created_at"].map(name => [name, fields.get(name) ?? ""]));
        if (payload.created_at === "")
            payload.created_at = null;
        try {
            await writeProject(apiUrl, "POST", payload);
            addForm.reset();
            document.getElementById("add-modal")?.hidePopover();
            showToast("Success", "Project created.", "success");
            await fetchProjects(searchInput.value.trim());
        }
        catch (error) {
            showToast("Could not create project", error instanceof Error ? error.message : "Request failed.", "error");
        }
        finally {
            button.disabled = false;
        }
    });
    projectGrid.addEventListener("click", async (event) => {
        if (!(event.target instanceof Element))
            return;
        const button = event.target.closest("button[data-action]");
        if (!button || button.disabled)
            return;
        const action = button.dataset.action;
        const id = button.dataset.id;
        if (!apiUrl || !id || (action !== "star" && action !== "delete"))
            return;
        if (action === "delete" && !window.confirm("Delete this project?"))
            return;
        button.disabled = true;
        try {
            const detailUrl = `${apiUrl}${encodeURIComponent(id)}/`;
            await writeProject(action === "star" ? `${detailUrl}star/` : detailUrl, action === "star" ? "POST" : "DELETE");
            showToast("Success", action === "star" ? "Star updated." : "Project deleted.", "success");
            await fetchProjects(searchInput.value.trim());
        }
        catch (error) {
            showToast("Request failed", error instanceof Error ? error.message : "Request failed.", "error");
        }
        finally {
            button.disabled = false;
        }
    });
    searchInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => fetchProjects(searchInput.value.trim()), 300);
    });
    fetchProjects(searchInput.value.trim());
});
