// Central state management
const appState = {
    currentScreen: 'landing',
    storyData: null, // response data from generation
};

// Available screens (imported via HTML scripts)
const screens = {
    landing: renderLandingContent,
    form: renderFormContent,
    loading: renderLoadingContent,
    output: renderOutputContent,
    history: renderHistoryContent,
    profile: renderProfileContent
};

// Navigation logic
function navigate(screenName) {
    if (!screens[screenName]) return;
    
    appState.currentScreen = screenName;
    const contentMount = document.getElementById('app-content');
    
    // Animate transition out
    contentMount.innerHTML = '';
    
    // Update bottom navigation active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('onclick') === `navigate('${screenName}')`) {
            item.classList.add('active');
        }
    });

    // Render new content
    const content = typeof screens[screenName] === 'function' ? screens[screenName]() : '';
    contentMount.innerHTML = `<div class="screen-enter">${content}</div>`;
    
    // Call mount hook if exists
    if (window[`mount_${screenName}`]) {
        window[`mount_${screenName}`]();
    }
}

// Initial mount
document.addEventListener('DOMContentLoaded', () => {
    navigate('landing');
});
