// its okay i guess
document.addEventListener("DOMContentLoaded", () => 
{
    const grid        = document.getElementById("grid")
    const template    = document.getElementById("card-template") as HTMLTemplateElement | null
    const searchInput = document.getElementById("search-input") as HTMLInputElement | null

    if (!(grid instanceof HTMLUListElement) || !template || !searchInput) return

    const render = (item: ApiItem): HTMLLIElement => 
    {
        const values: Record<string, unknown> = { ...item }
    
        for (const key of ["started_at", "ended_at", "created_at"]) 
        {
            const value = item[key]
        
            if (value) 
            {
                const date = new Date(String(value))
            
                values[`${key}_iso`] = Number.isNaN(date.getTime()) ? "" : date.toISOString()
                values[key]          = Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("en-US", { year: "numeric", month: "long" }).format(date)
            }
        }
        
        values.star_button = item.is_starred ? "❀ Prune a flower" : "✿ Bloom a flower"
        values.star_title  = item.starred_by_names || "Be the first to bloom"

        const html = template.innerHTML.replace(/\[\[\s*(\w+)\s*\]\]/g, (_match, key: string) => escapeHtml(values[key]))
        const doc  = new DOMParser().parseFromString(html, "text/html")
        
        const card = doc.body.firstElementChild
        
        if (!(card instanceof HTMLLIElement)) throw new Error("Card template must have an <li> root.")
        
        card.querySelectorAll<HTMLAnchorElement>("a[href]").forEach(link => 
        {
            if (!link.getAttribute("href")) 
            { 
                link.removeAttribute("href") 
                return 
            }
            
            try 
            {
                const url = new URL(link.getAttribute("href") || "", window.location.origin)
            
                if (!["http:", "https:"].includes(url.protocol)) link.removeAttribute("href")
            } 
            
            catch 
            { 
                link.removeAttribute("href")
            }
        })
        
        card.querySelectorAll<HTMLImageElement>("img[src]").forEach(image => 
        {
            if (!image.getAttribute("src")) 
            { 
                image.removeAttribute("src")
        
                return 
            }
            
            try 
            {
                const url = new URL(image.getAttribute("src") || "", window.location.origin)
            
                if (!["http:", "https:"].includes(url.protocol)) image.removeAttribute("src")
            } 
            
            catch 
            { 
                image.removeAttribute("src") 
            }
        })
        
        return card
    }

    const addForm   = document.getElementById("add-form") as HTMLFormElement | null
    const editForm  = document.getElementById("edit-form") as HTMLFormElement | null
    const editModal = document.getElementById("edit-modal") as (HTMLElement & { showPopover(): void; hidePopover(): void }) | null
    
    const apiUrl = grid.dataset.apiUrl
    
    if (!apiUrl) return

    void initAjaxList({
        grid,
    
        apiUrl,
        csrfToken: grid.dataset.csrf || "",
    
        searchInput,
        addForm,
        editForm,
        editModal,
        
        canDelete: grid.dataset.isSuperuser === "true",
        isAuthenticated: grid.dataset.isAuthenticated === "true",
    
        render,
    })
})
