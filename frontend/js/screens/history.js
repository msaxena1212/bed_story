function renderHistoryContent() {
    // We trigger the fetch immediately and update the DOM when ready
    setTimeout(fetchHistory, 0);

    return `
        <div class="container mt-4" style="padding-bottom: 5rem;">
            <h2>Your Stories 📚</h2>
            <p class="mt-2 text-primary">Relive the magic!</p>
            
            <div id="history-list" class="mt-4" style="display:flex; flex-direction:column; gap: 1rem;">
                <div class="text-center" style="padding: 3rem;">
                    <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2rem; color: var(--secondary);"></i>
                    <p class="mt-2">Loading your adventures...</p>
                </div>
            </div>
        </div>
    `;
}

async function fetchHistory() {
    const list = document.getElementById('history-list');
    if (!list) return;

    try {
        const response = await fetch('/stories');
        const stories = await response.json();

        if (stories.length === 0) {
            list.innerHTML = `
                <div class="text-center" style="padding: 3rem; background: white; border-radius: var(--radius);">
                    <p>No stories saved yet. Create your first one!</p>
                    <button class="btn-primary mt-2" onclick="navigate('form')">Get Started</button>
                </div>
            `;
            return;
        }

        list.innerHTML = stories.map(story => `
            <div onclick="viewHistoryItem(${JSON.stringify(story).replace(/"/g, '&quot;')})" style="background: white; padding: 15px; border-radius: var(--radius); display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); cursor: pointer; transition: transform 0.2s;">
                <div style="width: 70px; height: 70px; background: ${getThemeColor(story.theme)}; border-radius: 12px; overflow: hidden; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    ${story.image_url ? 
                        `<img src="${story.image_url}" style="width: 100%; height: 100%; object-fit: cover;">` : 
                        `<i class="fa-solid ${getThemeIcon(story.theme)}" style="color: white; font-size: 1.5rem;"></i>`
                    }
                </div>
                <div style="flex-grow: 1;">
                    <h4 style="margin: 0; font-size: 1rem;">${story.name}'s Adventure</h4>
                    <p style="font-size: 0.8rem; margin: 0; color: #888;">${story.theme} • ${new Date(story.created_at).toLocaleDateString()}</p>
                </div>
                <button class="icon-btn">
                    <i class="fa-solid fa-chevron-right"></i>
                </button>
            </div>
        `).join('');

    } catch (err) {
        console.error(err);
        list.innerHTML = `<p class="text-center text-danger">Error loading history. Make sure the backend is running.</p>`;
    }
}

function viewHistoryItem(story) {
    appState.storyData = story;
    navigate('output');
}

function getThemeIcon(theme) {
    const icons = {
        'Space': 'fa-rocket',
        'Jungle': 'fa-leaf',
        'Magic': 'fa-wand-sparkles',
        'Ocean': 'fa-fish',
        'Adventure': 'fa-map'
    };
    return icons[theme] || 'fa-book';
}

function getThemeColor(theme) {
    const colors = {
        'Space': '#6c5ce7',
        'Jungle': '#00b894',
        'Magic': '#fd79a8',
        'Ocean': '#0984e3',
        'Adventure': '#e17055'
    };
    return colors[theme] || 'var(--primary)';
}
