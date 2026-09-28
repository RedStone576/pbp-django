"use strict";
function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, meow => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[meow]);
}
async function initAjaxList(config) {
    const { apiUrl, containerId, searchInputId, addFormId, modalId, renderCard } = config;
    const container = document.getElementById(containerId);
    const searchInput = document.getElementById(searchInputId);
    const addForm = document.getElementById(addFormId);
    if (!container || !apiUrl)
        return;
    const listContainer = container;
    const baseUrl = apiUrl;
    let abortCtrl;
    let debounceTimer;
    async function loadData(query = "") {
        abortCtrl?.abort();
        abortCtrl = new AbortController();
        try {
            const url = query ? `${baseUrl}?title=${encodeURIComponent(query)}` : baseUrl;
            const res = await fetch(url, {
                headers: { "Accept": "application/json" },
                signal: abortCtrl.signal
            });
            if (!res.ok)
                throw new Error("Network err");
            const data = await res.json();
            listContainer.innerHTML = "";
            if (data.length === 0) {
                listContainer.innerHTML = '<p class="dinkus">Nothing.</p>';
                return;
            }
            data.forEach(item => {
                const li = document.createElement("li");
                li.innerHTML = renderCard(item);
                listContainer.appendChild(li);
            });
        }
        catch (e) {
            if (e instanceof DOMException && e.name === "AbortError")
                return;
            console.error(e);
        }
    }
    searchInput?.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            loadData(searchInput.value.trim());
        }, 300);
    });
    addForm?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const btn = addForm.querySelector('button[type="submit"]');
        if (!btn)
            return;
        btn.disabled = true;
        try {
            const res = await fetch(baseUrl, {
                method: "POST",
                body: new FormData(addForm),
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            const result = await res.json().catch(() => ({}));
            if (res.ok) {
                addForm.reset();
                if (modalId)
                    document.getElementById(modalId)?.hidePopover();
                if (typeof showToast !== "undefined")
                    showToast("Success", "Entry added successfully!", "success");
                loadData(searchInput?.value.trim() ?? "");
            }
            else {
                const errs = result.errors ? Object.values(result.errors).flat().map(e => e.message) : ["Error saving."];
                if (typeof showToast !== "undefined")
                    showToast("Failed", errs.join(" "), "error");
            }
        }
        finally {
            btn.disabled = false;
        }
    });
    listContainer.addEventListener("submit", async (e) => {
        const form = e.target;
        if (!(form instanceof HTMLFormElement))
            return;
        e.preventDefault();
        if (form.classList.contains("delete-form") && !confirm("Delete this entry?"))
            return;
        try {
            const res = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            if (res.ok) {
                if (form.classList.contains("delete-form")) {
                    if (typeof showToast !== "undefined") {
                        showToast("Deleted", "Entry removed.", "success");
                    }
                }
                loadData(searchInput?.value.trim() ?? "");
            }
            else if (res.status === 403) {
                if (typeof showToast !== "undefined") {
                    showToast("Denied", "Permission denied.", "error");
                }
            }
        }
        catch (err) {
            console.error(err);
        }
    });
    loadData(searchInput?.value.trim() ?? "");
}
