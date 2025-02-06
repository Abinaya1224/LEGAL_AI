window.onload = function() {
    const emptyState = document.getElementById('empty-state');
    const contentArea = document.getElementById('content-area');

    // Assuming `recent_files` is passed from the backend
    if (recent_files.length > 0) {
        emptyState.classList.add('d-none');
        contentArea.classList.remove('d-none');
    } else {
        emptyState.classList.remove('d-none');
        contentArea.classList.add('d-none');
    }
};
