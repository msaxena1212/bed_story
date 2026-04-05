function renderFormContent() {
    return `
        <div class="container mt-4" style="padding-top: 1rem; padding-bottom: 4rem;">
            <h2>Tell us about your child 👶</h2>
            <p class="mt-2" style="margin-bottom: 2rem;">We'll craft a personalized adventure!</p>

            <form id="storyForm" onsubmit="handleFormSubmit(event)">
                <div class="form-group">
                    <label>Child's Name</label>
                    <input type="text" class="form-control" id="childName" placeholder="e.g. Aarav" required>
                </div>
                
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" class="form-control" id="childAge" min="2" max="12" placeholder="e.g. 5" required>
                </div>

                <div class="form-group">
                    <label>Theme</label>
                    <select class="form-control" id="storyTheme">
                        <option value="Jungle">Jungle Safari</option>
                        <option value="Space">Space Explorer</option>
                        <option value="Magic">Magical Kingdom</option>
                        <option value="Ocean">Deep Ocean</option>
                        <option value="Adventure">City Adventure</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Mood</label>
                    <select class="form-control" id="storyMood">
                        <option value="Calm">Calm & Sleepy</option>
                        <option value="Funny">Funny & Silly</option>
                        <option value="Adventurous">Adventurous</option>
                    </select>
                </div>

                <div class="form-group" style="flex-direction: row; justify-content: space-between; align-items: center; background: white; padding: 15px; border-radius: var(--radius);">
                    <label style="margin: 0;">Include a Learning Message?</label>
                    <input type="checkbox" id="includeLearning" style="transform: scale(1.5);" checked>
                </div>

                <button type="submit" class="btn-primary" style="margin-top: 2rem;">
                    Generate Story 🎧
                </button>
            </form>
        </div>
    `;
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const payload = {
        name: document.getElementById('childName').value,
        age: parseInt(document.getElementById('childAge').value, 10),
        theme: document.getElementById('storyTheme').value,
        mood: document.getElementById('storyMood').value,
        learning: document.getElementById('includeLearning').checked
    };

    // 1. Transition to Loading Screen
    navigate('loading');
    
    try {
        // Prepare global state for live stream
        appState.storyData = {
            name: payload.name,
            theme: payload.theme,
            story_text: "",
            audio_url: "",
            video_url: "",
            parent_tip: "",
            image_url: ""
        };

        // 2. Fetch with Streaming Response
        const response = await fetch('http://127.0.0.1:8000/generate-story', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error('API Error');
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        // Immediately switch to 'output' screen
        navigate('output');
        
        let fullText = "";
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, {stream: true});
            fullText += chunk;
            
            // Robustly extract the story text by only pruning confirmed metadata sections
            let displayStory = fullText;
            
            // Only split if the full delimiter is present to avoid pruning decorative dashes
            if (fullText.includes("---PARENT TIP---")) {
                displayStory = fullText.split("---PARENT TIP---")[0];
            } else if (fullText.includes("---SEARCH KEYWORDS---")) {
                displayStory = fullText.split("---SEARCH KEYWORDS---")[0];
            } else if (fullText.includes("---IMAGE URL---")) {
                displayStory = fullText.split("---IMAGE URL---")[0];
            }
            
            appState.storyData.story_text = displayStory.trim();
            
            // Find and update the story text block directly for live feel
            const storyOutput = document.querySelector('.mt-4[style*="white-space: pre-wrap"]');
            if (storyOutput) {
                storyOutput.innerText = appState.storyData.story_text;
            }
        }

        // 3. Final Parse & Content Reveal (Parent Tips, Images, etc.)
        if (fullText.includes("---PARENT TIP---")) {
            const parts = fullText.split("---PARENT TIP---");
            if (parts.length > 1) {
                const extra = parts[1].split("---SEARCH KEYWORDS---");
                appState.storyData.parent_tip = extra[0].trim();
                
                if (extra.length > 1) {
                    const imgParts = extra[1].split("---IMAGE URL---");
                    if (imgParts.length > 1) {
                        appState.storyData.image_url = imgParts[1].trim();
                    }
                }
            }
        }

        // Re-render one last time to ensure everything (images, tips) is perfect
        navigate('output');

    } catch (err) {
        console.error("Streaming Error:", err);
        alert('Magical connection failed. Make sure the backend is running!');
        navigate('form');
    }
}
