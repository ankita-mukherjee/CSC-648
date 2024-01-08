// Shows the checked tab's data
function showTab(tabName) {
    var tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(function(content) {
        content.style.display = 'none';
    });
    document.getElementById(tabName).style.display = 'block';

    localStorage.setItem('selectedTab', tabName);
}

// Shows the last selected tab
window.onload = function() {
    var lastSelectedTab = localStorage.getItem('selectedTab');
    if (lastSelectedTab) {
        var tabToSelect = document.getElementById(lastSelectedTab);
        if (tabToSelect) {
            tabToSelect.checked = true;
            showTab(lastSelectedTab);
        }
    } else {
        // If no tab is selected in local storage, default to "My Posts"
        var defaultTab = document.getElementById('tab1');
        defaultTab.checked = true;
        showTab('my_posts');
    }
};
