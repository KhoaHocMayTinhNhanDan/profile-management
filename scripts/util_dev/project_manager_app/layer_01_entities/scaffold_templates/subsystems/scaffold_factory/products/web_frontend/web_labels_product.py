from ..abstract.i_labels_product import AbstractLabels

class WebLabels(AbstractLabels):
    def get_template(self) -> str:
        return '''class HeaderLabel extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        const label = document.createElement('h2');
        label.textContent = this.getAttribute('text') || '';
        label.style = `
            color: #89b4fa;
            font-family: Inter, sans-serif;
            margin: 0 0 10px 0;
            font-size: 20px;
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
            color: #cdd6f4;
            font-family: Inter, sans-serif;
            margin: 0;
            font-size: 14px;
        `;
        shadow.appendChild(label);
    }
}
customElements.define('body-label', BodyLabel);
'''
