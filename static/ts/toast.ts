let toastTimer: ReturnType<typeof setTimeout>

function showToast(title: string, message: string, type: "success" | "error" = "success", duration: number = 3000): void 
{
    const toastComponent = document.getElementById("toast-component")
    const toastTitle     = document.getElementById("toast-title")
    const toastMessage   = document.getElementById("toast-message")
    const toastIcon      = document.getElementById("toast-icon")

    if (!toastComponent || !toastTitle || !toastMessage || !toastIcon) return

    toastTitle.textContent   = title
    toastMessage.textContent = message

    if (type === "success") 
    {
        toastIcon.textContent = "❀"
        toastIcon.style.color = "var(--foreground)"
    } 
    
    else 
    {
        toastIcon.textContent = "✿"
        toastIcon.style.color = "var(--link)"
    }

    clearTimeout(toastTimer)

    if (!toastComponent.matches(":popover-open")) 
    {
        toastComponent.showPopover()
    
        void toastComponent.offsetHeight // this is my first time seeing someone using void this way holy 
    }

    toastComponent.classList.remove("toast-hidden")
    toastComponent.classList.add("toast-show")

    toastTimer = setTimeout(() => 
    {
        toastComponent.classList.remove("toast-show")
        toastComponent.classList.add("toast-hidden")

        toastTimer = setTimeout(() => toastComponent.hidePopover(), 300)
    }, duration)
}
