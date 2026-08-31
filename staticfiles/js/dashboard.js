document.addEventListener('DOMContentLoaded', function() {
    var shell = document.querySelector('.dashboard-shell');
    var toggles = document.querySelectorAll('[data-sidebar-toggle]');

    if (!shell || !toggles || toggles.length === 0) return;

    function syncAria(expanded) {
        toggles.forEach(function(btn) {
            btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        });
    }

    var savedState = localStorage.getItem('dashboardSidebarCollapsed');
    var shouldCollapse = savedState === 'true';

    if (shouldCollapse) {
        shell.classList.add('sidebar-collapsed');
    } else {
        shell.classList.remove('sidebar-collapsed');
    }

    syncAria(!shouldCollapse);

    toggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            var collapsed = shell.classList.toggle('sidebar-collapsed');
            syncAria(!collapsed);
            localStorage.setItem('dashboardSidebarCollapsed', collapsed ? 'true' : 'false');
        });
    });
});

