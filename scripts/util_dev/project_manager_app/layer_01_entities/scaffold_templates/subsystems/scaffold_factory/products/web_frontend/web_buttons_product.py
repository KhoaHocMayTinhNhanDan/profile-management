from ..abstract.i_buttons_product import AbstractButtons

class WebButtons(AbstractButtons):
    def get_template(self) -> str:
        return '''class PrimaryButton extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const button = document.createElement('button');
        button.textContent = this.getAttribute('text') || 'Button';
        button.style = `
            background-color: #89b4fa;
            color: #11111b;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 13px;
            transition: background-color 0.2s;
        `;
        button.onmouseover = () => button.style.backgroundColor = '#b4befe';
        button.onmouseout = () => button.style.backgroundColor = '#89b4fa';
        shadow.appendChild(button);
    }
}
customElements.define('primary-button', PrimaryButton);
'''
