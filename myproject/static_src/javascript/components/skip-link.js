class SkipLink {
    static selector() {
        return '[data-skip-link]';
    }

    constructor(node) {
        this.skipLink = node;
        this.main = document.querySelector('main');

        if (this.skipLink && this.main) {
            this.skipLink.addEventListener('click', () => this.handleClick());
        }
    }

    handleClick() {
        this.main.setAttribute('tabindex', -1);
        this.main.addEventListener('blur', () => this.handleBlur());
        this.main.addEventListener('focusout', () => this.handleBlur());
        this.main.focus();
    }

    handleBlur() {
        this.main.removeAttribute('tabindex');
        this.main.removeEventListener('blur', this.handleBlur);
        this.main.removeEventListener('focusout', this.handleBlur);
    }
}

export default SkipLink;
