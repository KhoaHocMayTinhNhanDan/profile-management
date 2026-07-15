from ..abstract.i_inputs_product import AbstractInputs


class WebInputs(AbstractInputs):
    def get_template(self) -> str:
        return """class FormInput extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const input = document.createElement('input');
        input.placeholder = this.getAttribute('placeholder') || '';
        input.type = this.getAttribute('type') || 'text';
        input.style = `
            background-color: {{ CARD_BG }};
            color: {{ TEXT_COLOR }};
            border: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            border-radius: {{ RADIUS }};
            padding: {{ INPUT_PADDING }};
            font-size: {{ INPUT_FONT_SIZE }};
            outline: none;
            width: 100%;
            box-sizing: border-box;
        `;
        input.onfocus = () => input.style.border = '{{ BORDER_WIDTH }} solid {{ ACCENT_COLOR }}';
        input.onblur = () => input.style.border = '{{ BORDER_WIDTH }} solid {{ BORDER_COLOR }}';
        shadow.appendChild(input);
    }
}
customElements.define('form-input', FormInput);
"""
