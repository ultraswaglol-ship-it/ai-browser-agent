DOM_JS_SCRIPT = """
(() => {
    let elements = [];
    let idCounter = 1;

    function isVisible(el) {
        if (!el) return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && 
               style.visibility !== 'hidden' && 
               style.opacity !== '0' &&
               (el.offsetWidth > 0 || el.offsetHeight > 0);
    }

    document.querySelectorAll('[data-agent-id]').forEach(el => el.removeAttribute('data-agent-id'));

    const selectors = [
        'a[href]', 
        'button', 
        'input:not([type="hidden"])', 
        'textarea', 
        'select', 
        '[role="button"]', 
        '[role="link"]',
        '[tabindex]:not([tabindex="-1"])'
    ];

    document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (isVisible(el)) {
            // Получаем текст элемента
            let text = el.innerText || el.textContent || el.value || el.placeholder || el.getAttribute('aria-label') || "";
            text = text.replace(/\\s+/g, ' ').trim();

            if (!text && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) {
                const id = el.id;
                if (id) {
                    const label = document.querySelector(`label[for="${id}"]`);
                    if (label) text = label.innerText.trim();
                }
            }
            
            if (!text && el.tagName === 'BUTTON') text = "Button (No text)";

            if (text.length > 50) text = text.substring(0, 50) + "...";

            el.setAttribute('data-agent-id', idCounter);
            
            elements.push(`[${idCounter}] <${el.tagName.toLowerCase()}> ${text}`);
            idCounter++;
        }
    });

    return elements.join('\\n');
})();
"""