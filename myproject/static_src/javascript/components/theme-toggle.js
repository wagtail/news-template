class ThemeToggle {
    static selector() {
        return '[data-theme-toggle]';
    }
    
    constructor(node) {
        this.toggleSwitch = node;
        this.currentTheme = localStorage.getItem('theme');

        if (this.currentTheme) {
            document.documentElement.classList.add('theme', this.currentTheme);
            if (this.currentTheme === 'dark') {
                this.toggleSwitch.checked = true;
            }
        }
        this.bindEvents()
    }

    bindEvents() {
        this.toggleSwitch.addEventListener('change', this.switchTheme, false);
    }

    switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.classList.add('theme', 'dark');
            document.documentElement.classList.remove('theme', 'light');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.add('theme', 'light');
            document.documentElement.classList.remove('theme', 'dark');
            localStorage.setItem('theme', 'light');
        }
    }
}

export default ThemeToggle;