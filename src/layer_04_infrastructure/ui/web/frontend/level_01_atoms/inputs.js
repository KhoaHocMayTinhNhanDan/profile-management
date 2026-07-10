class FormInput extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const input = document.createElement('input');
        input.placeholder = this.getAttribute('placeholder') || '';
        input.type = this.getAttribute('type') || 'text';
        input.style = `
            background-color: #181825;
            color: #cdd6f4;
            border: 1px solid #313244;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            outline: none;
            width: 100%;
            box-sizing: border-box;
        `;
        input.onfocus = () => input.style.border = '1px solid #89b4fa';
        input.onblur = () => input.style.border = '1px solid #313244';
        shadow.appendChild(input);
    }
}
customElements.define('form-input', FormInput);
