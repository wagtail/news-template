import Shepherd from 'shepherd.js';
import 'shepherd.js/dist/css/shepherd.css';
import '../../sass/admin/onboarding.scss';

/**
 * Safely query a selector, returning null if the element is not present.
 * Used to gracefully handle cases where a step's target might not exist.
 *
 * @param {string} selector
 * @returns {Element|null}
 */
function findElement(selector) {
    try {
        return document.querySelector(selector);
    } catch {
        return null;
    }
}

/**
 * Build and return a configured Shepherd Tour instance.
 *
 * @returns {Shepherd.Tour}
 */
function createTour() {
    const tour = new Shepherd.Tour({
        useModalOverlay: true,
        keyboardNavigation: true,
        defaultStepOptions: {
            classes: 'wagtail-onboarding-step',
            scrollTo: { behavior: 'smooth', block: 'center' },
            cancelIcon: {
                enabled: true,
                label: 'Close tour',
            },
            modalOverlayOpeningPadding: 8,
            modalOverlayOpeningRadius: 4,
            when: {
                show() {
                    const el = this.getElement();
                    if (el) {
                        el.setAttribute('role', 'dialog');
                        el.setAttribute('aria-modal', 'true');
                        el.setAttribute(
                            'aria-label',
                            this.options.title || 'Onboarding step',
                        );
                    }
                },
            },
        },
    });

    tour.addStep({
        id: 'welcome',
        title: 'Welcome to the News Template',
        text: 'This template already contains demo content. This tour will quickly introduce the admin interface.',
        buttons: [
            {
                text: 'Skip tour',
                action: tour.cancel,
                classes: 'shepherd-button-secondary',
                secondary: true,
            },
            {
                text: 'Next',
                action: tour.next,
            },
        ],
    });



    const dashboardSelectors = [
        '[data-nav-primary-link="dashboard"]',
        'a[href*="/admin/"][aria-label*="ashboard"]',
        '.sidebar-nav-item a[href$="/admin/"]',
        '.sidebar__inner a:first-of-type',
    ];
    const dashboardEl = dashboardSelectors.reduce(
        (found, sel) => found || findElement(sel),
        null,
    );

    tour.addStep({
        id: 'dashboard',
        title: 'Dashboard',
        text: 'The dashboard gives you a quick overview of recent activity and shortcuts to common tasks.',
        ...(dashboardEl ? { attachTo: { element: dashboardEl, on: 'right' } } : {}),
        buttons: [
            {
                text: 'Back',
                action: tour.back,
                classes: 'shepherd-button-secondary',
                secondary: true,
            },
            {
                text: 'Next',
                action: tour.next,
            },
        ],
    });

    const sidebarSelectors = [
        'nav[aria-label]',
        '.sidebar',
        '[data-controller="w-sidebar"]',
        '.sidebar__inner',
    ];
    const sidebarEl = sidebarSelectors.reduce(
        (found, sel) => found || findElement(sel),
        null,
    );

    tour.addStep({
        id: 'sidebar',
        title: 'Navigation Sidebar',
        text: [
            'Use the sidebar to navigate the admin.',
            '<ul style="margin-top:0.5em;padding-left:1.2em;list-style:disc">',
            '  <li><strong>Pages</strong> — manage all pages in your site hierarchy</li>',
            '  <li><strong>Snippets</strong> — manage reusable content pieces</li>',
            '</ul>',
            '<p style="margin-top:0.5em">',
            '  <em>Articles</em> are <strong>Pages</strong>. ',
            '  <em>Authors</em> and <em>Article Topics</em> are <strong>Snippets</strong>.',
            '</p>',
        ].join(''),
        ...(sidebarEl ? { attachTo: { element: sidebarEl, on: 'right' } } : {}),
        buttons: [
            {
                text: 'Back',
                action: tour.back,
                classes: 'shepherd-button-secondary',
                secondary: true,
            },
            {
                text: 'Next',
                action: tour.next,
            },
        ],
    });


    const pagesSelectors = [
        '[data-nav-primary-link="pages"]',
        'a[href*="/admin/pages/"]',
        '.sidebar-nav-item a[href*="/pages/"]',
    ];
    const pagesEl = pagesSelectors.reduce(
        (found, sel) => found || findElement(sel),
        null,
    );

    tour.addStep({
        id: 'pages',
        title: 'Pages — Your Content Explorer',
        text: 'All new content is managed from the page explorer. Click <strong>Pages</strong> to browse the site hierarchy and create or edit articles.',
        ...(pagesEl ? { attachTo: { element: pagesEl, on: 'right' } } : {}),
        buttons: [
            {
                text: 'Back',
                action: tour.back,
                classes: 'shepherd-button-secondary',
                secondary: true,
            },
            {
                text: 'Next',
                action: tour.next,
            },
        ],
    });


    tour.addStep({
        id: 'finish',
        title: "You're all set!",
        text: 'Open an existing Article to continue exploring the editor. You can find articles under <strong>Pages</strong> in the sidebar.',
        buttons: [
            {
                text: 'Back',
                action: tour.back,
                classes: 'shepherd-button-secondary',
                secondary: true,
            },
            {
                text: 'Done',
                action: tour.complete,
            },
        ],
    });

    return tour;
}


function initOnboardingTour() {
    const path = window.location.pathname.replace(/\/$/, '');
    const isAdminDashboard =
        path === '/admin' ||
        path.endsWith('/admin') ||
        /\/admin\/?$/.test(path);

    if (!isAdminDashboard) {
        return;
    }

    const tour = createTour();
    tour.start();
}

document.addEventListener('DOMContentLoaded', initOnboardingTour);
