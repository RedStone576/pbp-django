"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("grid");
    const templateElement = document.getElementById("card-template");
    if (!grid || !templateElement)
        return;
    const templateStr = templateElement.innerHTML;
    const apiUrl = grid.getAttribute("data-api-url");
    const createUrl = grid.getAttribute("data-create-url");
    const csrf = grid.getAttribute("data-csrf");
    const isSuperuser = grid.getAttribute("data-is-superuser") === "true";
    const isEditor = grid.getAttribute("data-is-editor") === "true";
    initAjaxList({
        apiUrl,
        containerId: "grid",
        searchInputId: "search-input",
        addFormId: "add-form",
        modalId: "add-modal",
        renderCard(item) {
            let html = templateStr;
            const fields = item.fields;
            const pk = item.pk;
            html = html.replace(/\[\[ pk \]\]/g, pk);
            html = html.replace(/\[\[ csrf \]\]/g, csrf || "");
            html = html.replace(/\[\[ createUrl \]\]/g, createUrl || "");
            for (const key of Object.keys(fields)) {
                let val = fields[key];
                if (key.endsWith("_at") && val) {
                    val = new Intl.DateTimeFormat("en-US", { year: "numeric", month: "long" }).format(new Date(val));
                }
                html = html.replace(new RegExp(`\\[\\[ ${key} \\]\\]`, 'g'), escapeHtml(val));
            }
            if (fields.is_starred !== undefined) {
                const starBtnText = fields.is_starred ? "❀ Prune a flower" : "✿ Bloom a flower";
                const starTitle = fields.star_count > 0 ? `Bloomed by ${escapeHtml(fields.starred_by_names)}` : "Be the first to bloom";
                html = html.replace(/\[\[ starBtnText \]\]/g, starBtnText);
                html = html.replace(/\[\[ starTitle \]\]/g, starTitle);
            }
            html = html.replace(/\[\[ .*? \]\]/g, "");
            return html;
        }
    });
});
