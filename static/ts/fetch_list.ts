interface AjaxListItem
{
    pk: string
}

interface AjaxListConfig<T extends AjaxListItem>
{
    apiUrl: string | null
    containerId: string
    searchInputId: string
    addFormId: string
    modalId?: string
    render: (item: T) => string
}

interface AjaxListResponse
{
    errors?: Record<string, Array<{ message: string }>>
}

function escapeHtml(value: unknown): string
{
    return String(value ?? "").replace(/[&<>"']/g, meow => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[meow]!)
}

async function initAjaxList<T extends AjaxListItem>(config: AjaxListConfig<T>): Promise<void>
{
    const { apiUrl, containerId, searchInputId, addFormId, modalId, render } = config

    const container   = document.getElementById(containerId)
    const searchInput = document.getElementById(searchInputId) as HTMLInputElement | null
    const addForm     = document.getElementById(addFormId) as HTMLFormElement | null

    if (!container || !apiUrl) return

    const listContainer = container
    const baseUrl = apiUrl

    const loadingState = document.getElementById("loading")
    const errorState   = document.getElementById("error")
    const emptyState   = document.getElementById("empty")

    let abortCtrl: AbortController | undefined
    let debounceTimer: ReturnType<typeof setTimeout> | undefined

    async function loadData(query = ""): Promise<void>
    {
        abortCtrl?.abort()
        abortCtrl = new AbortController()

        try 
        {
            if (loadingState) loadingState.style.display = "block"
            if (errorState)   errorState.style.display   = "none"
            if (emptyState)   emptyState.style.display   = "none"
            
            listContainer.style.display = "none"
            
            const url = query ? `${baseUrl}?title=${encodeURIComponent(query)}` : baseUrl

            const res = await fetch(url, {
                headers: { "Accept": "application/json" },
                signal: abortCtrl.signal
            })

            if (!res.ok) throw new Error("Network err")

            const data: T[] = await res.json()

            
            if (loadingState) loadingState.style.display = "none"
            
            listContainer.innerHTML = ""

            if (data.length === 0) 
            {
                if (emptyState) emptyState.style.display = "block"
                else listContainer.innerHTML = '<p class="dinkus">Nothing.</p>'
                
                return
            }

            listContainer.style.display = "block"
            data.forEach(item => 
            {
                const li = document.createElement("li")
            
                li.innerHTML = render(item)
            
                listContainer.appendChild(li)
            })
        } 
        
        catch (e) 
        {
            if (e instanceof DOMException && e.name === "AbortError") return
            
            if (loadingState) loadingState.style.display = "none"
            if (errorState) errorState.style.display     = "block"
        
            console.error(e)
        }
    }

    searchInput?.addEventListener("input", () => 
    {
        clearTimeout(debounceTimer)

        debounceTimer = setTimeout(() => 
        {
            loadData(searchInput.value.trim())
        }, 300)
    })

    addForm?.addEventListener("submit", async e => 
    {
        e.preventDefault()

        const btn = addForm.querySelector<HTMLButtonElement>('button[type="submit"]')

        if (!btn) return

        btn.disabled = true

        try 
        {
            const res = await fetch(baseUrl, {
                method: "POST",
                body: new FormData(addForm),
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })

            const result: AjaxListResponse = await res.json().catch(() => ({}))

            if (res.ok) 
            {
                addForm.reset()

                if (modalId) document.getElementById(modalId)?.hidePopover()
                if (typeof showToast !== "undefined") showToast("Success", "Entry added successfully!", "success")

                loadData(searchInput?.value.trim() ?? "")
            } 
            
            else 
            {
                const errs = result.errors ? Object.values(result.errors).flat().map(e => e.message) : ["Error saving."]

                if (typeof showToast !== "undefined") showToast("Failed", errs.join(" "), "error")
            }
        } 
        
        finally 
        {
            btn.disabled = false
        }
    })

    listContainer.addEventListener("submit", async e => 
    {
        const form = e.target

        if (!(form instanceof HTMLFormElement)) return

        e.preventDefault()

        if (form.classList.contains("delete-form") && !confirm("Delete this entry?")) return

        try 
        {
            const res = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })

            if (res.redirected && res.url.includes("login")) 
            {
                window.location.href = res.url
                return
            }

            if (res.ok) 
            {
                if (form.classList.contains("delete-form")) 
                {
                    if (typeof showToast !== "undefined") 
                    {
                        showToast("Deleted", "Entry removed.", "success")
                    }
                }

                loadData(searchInput?.value.trim() ?? "")
            } 
            
            else if (res.status === 403) 
            {
                if (typeof showToast !== "undefined") 
                {
                    showToast("Denied", "Permission denied.", "error")
                }
            }
        } 
        
        catch (err) 
        {
            console.error(err)
        }
    })

    loadData(searchInput?.value.trim() ?? "")
}
