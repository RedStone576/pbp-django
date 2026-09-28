let toastTimer;

function showToast(title, message, type = 'success', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toastComponent) return;

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    if (type === 'success') {
        toastIcon.textContent = '❀';
        toastIcon.style.color = 'var(--foreground)';
    } else {
        toastIcon.textContent = '✿';
        toastIcon.style.color = 'var(--link)';
    }

    clearTimeout(toastTimer);

    if (!toastComponent.matches(':popover-open')) {
        toastComponent.showPopover();
        void toastComponent.offsetHeight;
    }

    toastComponent.classList.remove('toast-hidden');
    toastComponent.classList.add('toast-show');

    toastTimer = setTimeout(() => {
        toastComponent.classList.remove('toast-show');
        toastComponent.classList.add('toast-hidden');
        toastTimer = setTimeout(() => toastComponent.hidePopover(), 300);
    }, duration);
}
