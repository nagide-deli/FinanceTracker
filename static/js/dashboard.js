function showSection(sectionId) {
    // Get all sections in the main content area
    const sections = document.querySelectorAll('.container ');

    // Loop through all sections
    sections.forEach((section) => {
        // If the section's ID matches the clicked link's target, show it
        if (section.id === sectionId) {
            section.style.display = 'block'; // Show the section
        } else {
            section.style.display = 'none'; // Hide other sections
        }
    });
    window.onload = function() {
    showSection('dashboard'); // Default section to display
};
}
