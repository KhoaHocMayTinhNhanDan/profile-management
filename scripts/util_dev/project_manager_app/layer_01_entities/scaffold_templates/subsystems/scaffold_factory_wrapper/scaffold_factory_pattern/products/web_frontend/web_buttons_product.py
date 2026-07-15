from ..abstract.i_buttons_product import AbstractButtons


class WebButtons(AbstractButtons):
    def get_template(self) -> str:
        return """class PrimaryButton extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const button = document.createElement('button');
        button.textContent = this.getAttribute('text') || 'Button';
        button.style = `
            background-color: {{ ACCENT_COLOR }};
            color: {{ SIDEBAR_BG }};
            font-weight: bold;
            padding: {{ BUTTON_PADDING }};
            border-radius: {{ RADIUS }};
            border: none;
            cursor: pointer;
            font-size: {{ BUTTON_FONT_SIZE }};
            transition: background-color {{ TRANSITION_DURATION }};
        `;
        button.onmouseover = () => button.style.backgroundColor = '{{ ACCENT_HOVER }}';
        button.onmouseout = () => button.style.backgroundColor = '{{ ACCENT_COLOR }}';
        shadow.appendChild(button);
    }
}
customElements.define('primary-button', PrimaryButton);
"""
