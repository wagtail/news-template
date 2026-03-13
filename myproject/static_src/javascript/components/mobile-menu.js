import { hideDropdownElement } from './utils';

class MobileMenu {
    static selector() {
        return '[data-mobile-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.mobileMenu = document.querySelector('[data-mobile-menu-content]');
        this.headerLogo = document.querySelector('[data-header-logo]');

        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', () => {
            if (this.mobileMenu.classList.contains('invisible')) {
                this.open();
            } else {
                this.close();
            }
        });
    }

    open() {
        // Set the menu button to be a cross.
        this.node.classList.add('mobile-menu-is-open');
        this.headerLogo.classList.add('mobile-menu-is-open');
        this.node.setAttribute('aria-expanded', 'true');
        this.node.setAttribute('aria-label', 'close navigation menu');
        this.body.classList.add('no-scroll');

        // Make sure that the page is not scrollable. Only the drawer.
        document.body.style.overflowY = 'hidden';

        // Open the mobile menu. Mobile menu slides from the right.
        this.mobileMenu.classList.remove('invisible');
        this.mobileMenu.classList.remove('translate-x-full');
        this.mobileMenu.classList.add('translate-x-0');

        // Focus on the first link in the mobile menu.
        const firstItem = this.mobileMenu.querySelector('a');
        firstItem?.focus();
    }

    close() {
        // Set the cross button to be a menu button.
        this.node.classList.remove('mobile-menu-is-open');
        this.headerLogo.classList.remove('mobile-menu-is-open');
        this.node.setAttribute('aria-expanded', 'false');
        this.node.setAttribute('aria-label', 'Open navigation menu');
        this.body.classList.remove('no-scroll');

        // Set the page to be scrollable.
        document.body.style.overflowY = 'visible';

        // Close the mobile menu.
        this.mobileMenu.classList.add('invisible');
        this.mobileMenu.classList.add('translate-x-full');
        this.mobileMenu.classList.remove('translate-x-0');
    }
}

export default MobileMenu;
