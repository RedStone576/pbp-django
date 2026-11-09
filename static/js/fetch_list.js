"use strict";
function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    })[char]);
}
function apiDateInput(value) {
    if (!value)
        return "";
    const date = new Date(String(value));
    if (Number.isNaN(date.getTime()))
        return "";
    return new Date(date.getTime() - date.getTimezoneOffset() * 60_000).toISOString().slice(0, 16);
}
function apiDateValue(value) {
    if (!value)
        return null;
    const date = new Date(String(value));
    return Number.isNaN(date.getTime()) ? String(value) : date.toISOString();
}
function apiFormData(form) {
    const payload = {};
    for (const [rawName, value] of new FormData(form)) {
        if (rawName === "csrfmiddlewaretoken" || rawName === "id" || typeof value !== "string")
            continue;
        const name = rawName.startsWith("edit-") ? rawName.slice(5) : rawName;
        payload[name] = name.endsWith("_at") ? apiDateValue(value) : value;
    }
    return payload;
}
function apiErrorMessage(data, status) {
    if (data && typeof data === "object") {
        const messages = Object.values(data).flatMap(value => Array.isArray(value) ? value.map(String) : [String(value)]);
        if (messages.length)
            return messages.join(" ");
    }
    return `Request failed (HTTP ${status}).`;
}
async function initAjaxList(config) {
    const { grid, apiUrl, csrfToken, searchInput, addForm, editForm, editModal, render } = config;
    const loadingState = document.getElementById("loading");
    const errorState = document.getElementById("error");
    const emptyState = document.getElementById("empty");
    if (!loadingState || !errorState || !emptyState)
        return;
    const loading = loadingState;
    const error = errorState;
    const empty = emptyState;
    let abortController;
    let debounceTimer;
    let itemsById = new Map();
    function showState(state) {
        loading.style.display = state === "loading" ? "block" : "none";
        error.style.display = state === "error" ? "block" : "none";
        empty.style.display = state === "empty" ? "block" : "none";
        grid.style.display = state === "grid" ? "block" : "none";
    }
    async function fetchItems(query = "") {
        abortController?.abort();
        abortController = new AbortController();
        showState("loading");
        try {
            const url = new URL(apiUrl, window.location.origin);
            if (query)
                url.searchParams.set("title", query);
            const response = await fetch(url, {
                headers: { Accept: "application/json" },
                signal: abortController.signal,
            });
            if (!response.ok)
                throw new Error(`HTTP ${response.status}`);
            const items = await response.json();
            itemsById = new Map(items.map(item => [item.id, item]));
            grid.replaceChildren(...items.map(render));
            showState(items.length ? "grid" : "empty");
        }
        catch (error) {
            if (error instanceof DOMException && error.name === "AbortError")
                return;
            console.error(error);
            showState("error");
        }
    }
    async function write(url, method, payload) {
        const response = await fetch(url, {
            method,
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: payload ? JSON.stringify(payload) : undefined,
        });
        if (response.status === 204)
            return;
        const data = await response.json().catch(() => ({}));
        if (!response.ok)
            throw new Error(apiErrorMessage(data, response.status));
    }
    async function submitForm(form, url, method, modal) {
        const button = form.querySelector('button[type="submit"]');
        if (!button)
            return;
        button.disabled = true;
        try {
            await write(url, method, apiFormData(form));
            form.reset();
            modal?.hidePopover();
            showToast("Success", method === "POST" ? "Entry added." : "Entry updated.", "success");
            await fetchItems(searchInput.value.trim());
        }
        catch (error) {
            showToast("Request failed", error instanceof Error ? error.message : "Request failed.", "error");
        }
        finally {
            button.disabled = false;
        }
    }
    addForm?.addEventListener("submit", event => {
        event.preventDefault();
        void submitForm(addForm, apiUrl, "POST", document.getElementById("add-modal"));
    });
    editForm?.addEventListener("submit", event => {
        event.preventDefault();
        const id = editForm.querySelector("#edit-id")?.value;
        if (id)
            void submitForm(editForm, `${apiUrl}${encodeURIComponent(id)}/`, "PATCH", editModal);
    });
    grid.addEventListener("click", event => {
        if (!(event.target instanceof Element))
            return;
        const button = event.target.closest("button[data-action]");
        if (!button || button.disabled)
            return;
        const action = button.dataset.action;
        const id = button.dataset.id;
        if (!id)
            return;
        if (action === "edit") {
            const item = itemsById.get(id);
            if (!item || !editForm || !editModal)
                return;
            editForm.querySelector("#edit-id").value = id;
            for (const field of editForm.querySelectorAll("[name^='edit-']")) {
                const name = field.name.slice(5);
                field.value = name.endsWith("_at") ? apiDateInput(item[name]) : String(item[name] ?? "");
            }
            editModal.showPopover();
            return;
        }
        if (action !== "star" && action !== "delete")
            return;
        if (!config.isAuthenticated || (action === "delete" && !config.canDelete))
            return;
        if (action === "delete" && !window.confirm("Delete this entry?"))
            return;
        button.disabled = true;
        const detailUrl = `${apiUrl}${encodeURIComponent(id)}/`;
        void write(action === "star" ? `${detailUrl}star/` : detailUrl, action === "star" ? "POST" : "DELETE")
            .then(async () => {
            showToast("Success", action === "star" ? "Star updated." : "Entry deleted.", "success");
            await fetchItems(searchInput.value.trim());
        })
            .catch(error => showToast("Request failed", error instanceof Error ? error.message : "Request failed.", "error"))
            .finally(() => { button.disabled = false; });
    });
    searchInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => { void fetchItems(searchInput.value.trim()); }, 300);
    });
    void fetchItems(searchInput.value.trim());
}
