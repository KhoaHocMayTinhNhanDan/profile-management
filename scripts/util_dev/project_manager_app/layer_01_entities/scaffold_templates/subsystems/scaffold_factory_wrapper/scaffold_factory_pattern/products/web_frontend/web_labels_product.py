from ..abstract.i_labels_product import AbstractLabels


class WebLabels(AbstractLabels):
    def get_template(self) -> str:
        return """class HeaderLabel extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const label = document.createElement('h2');
        label.textContent = this.getAttribute('text') || '';
        label.style = `
            color: {{ ACCENT_COLOR }};
            font-family: '{{ FONT_FAMILY }}';
            margin: 0 0 {{ LABEL_MARGIN_BOTTOM }} 0;
            font-size: {{ HEADER_FONT_SIZE }};
        `;
        shadow.appendChild(label);
    }
}
customElements.define('header-label', HeaderLabel);

class BodyLabel extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const label = document.createElement('p');
        label.textContent = this.getAttribute('text') || '';
        label.style = `
            color: {{ TEXT_COLOR }};
            font-family: '{{ FONT_FAMILY }}';
            margin: 0;
            font-size: {{ BODY_FONT_SIZE }};
        `;
        shadow.appendChild(label);
    }
}
customElements.define('body-label', BodyLabel);
"""
