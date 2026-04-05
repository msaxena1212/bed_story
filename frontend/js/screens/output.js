function renderOutputContent() {
    // Determine data to show
    const data = appState.storyData || {
        name: "Child", 
        theme: "Magic", 
        story_text: "Once upon a time...",
        audio_url: "",
        video_url: ""
    };

    return `
        <div class="container mt-4" style="padding-bottom: 5rem;">
            <div class="text-center">
                <h2>Your Story is Ready 🎉</h2>
                <p class="mt-2 text-primary" style="font-weight: 600;">${data.name}'s ${data.theme} Adventure</p>
                
                <!-- Audio Generation Button - Moved to be very prominent -->
                <div class="mt-3" id="audio-gen-wrapper" style="display: ${data.audio_url ? 'none' : 'block'};">
                    <button id="audio-gen-btn" class="btn-primary" onclick="generateAudio()" 
                            style="background: var(--secondary); color: white; display: inline-flex; align-items: center; gap: 10px; padding: 12px 25px; border-radius: 30px; box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);">
                        <i class="fa-solid fa-microphone-lines"></i>
                        <span>Create Magic Voice ✨</span>
                    </button>
                </div>
            </div>

            <!-- Audio Player Block (Initially hidden until generated) -->
            <div id="audio-player-container" class="mt-3" style="display: ${data.audio_url ? 'block' : 'none'};">
                <div style="background: white; padding: 1.2rem; border-radius: var(--radius); box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="fa-solid fa-volume-high text-primary"></i>
                        <h4 style="margin: 0; font-size: 0.9rem;">Listen to the Caring Narrator</h4>
                    </div>
                    <audio id="story-audio" controls style="width: 100%; margin-top: 0.8rem;">
                        <source src="${data.audio_url}" type="audio/mpeg">
                    </audio>
                </div>
            </div>

            <div id="audio-loading" class="mt-3 text-center" style="display: none; background: #f8f9ff; padding: 1rem; border-radius: var(--radius); border: 2px dashed var(--secondary);">
                <i class="fa-solid fa-wand-sparkles fa-spin text-secondary" style="font-size: 1.5rem;"></i>
                <p class="mt-2" style="font-size: 0.9rem; font-weight: 600; color: var(--secondary);">Creating Magic Voice... 🎤</p>
                <p style="font-size: 0.7rem; color: #888;">This can take a minute on CPU</p>
            </div>

            <!-- Story Illustration (NEW) -->
            ${data.image_url ? `
            <div class="story-illustration">
                <img src="${data.image_url}" alt="Story Illustration" onerror="this.parentElement.innerHTML='<div class=\"illustration-placeholder\">The magic drawing is still being painted...</div>'">
            </div>
            ` : ''}

            <!-- Story Text Block -->
            <div class="mt-4" style="background: white; padding: 2rem; border-radius: var(--radius); box-shadow: 0 4px 15px rgba(0,0,0,0.03); line-height: 1.6; font-size: 1.1rem; white-space: pre-wrap;">
                ${data.story_text || 'The magical storyteller is gathering its thoughts and preparing your adventure... ✨'}
            </div>

            <!-- Parent Corner (New Emotional Detailing) -->
            <div class="mt-4" id="parent-corner" style="background: linear-gradient(135deg, #fff9f9 0%, #fff1f1 100%); padding: 1.5rem; border-radius: var(--radius); border: 2px solid #ff7675; box-shadow: 0 4px 15px rgba(255, 118, 117, 0.1);">
                <div style="display: flex; align-items: center; gap: 10px; color: #d63031;">
                    <i class="fa-solid fa-heart-pulse" style="font-size: 1.2rem;"></i>
                    <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700;">Parent's Corner ❤️</h3>
                </div>
                <p class="mt-2" style="font-style: italic; color: #444; line-height: 1.5; font-size: 0.95rem;">
                    ${data.parent_tip || 'A small moment of connection to end the day.'}
                </p>
                <div class="mt-2" style="font-size: 0.75rem; color: #888;">
                    Connection Tip: Use this to help your child feel secure and loved before they sleep.
                </div>
            </div>

            <!-- Actions -->
            <div class="mt-4" style="display: flex; gap: 1rem; flex-direction: column;">
                <div style="background: #e8f5e9; color: #2e7d32; padding: 12px; border-radius: var(--radius); text-align: center; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <i class="fa-solid fa-circle-check"></i>
                    Story automatically saved to History
                </div>
                
                <button class="btn-primary" onclick="navigate('form')" style="background: var(--secondary); color: white;">
                    Create Another Story
                </button>
            </div>
            
        </div>
    `;
}

async function generateAudio() {
    const btn = document.getElementById('audio-gen-btn');
    const loading = document.getElementById('audio-loading');
    const playerContainer = document.getElementById('audio-player-container');
    const player = document.getElementById('story-audio');
    
    if (!appState.storyData || !appState.storyData.story_text) return;

    btn.style.display = 'none';
    loading.style.display = 'block';

    try {
        const response = await fetch('/generate-audio', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                story_text: appState.storyData.story_text
            })
        });

        const data = await response.json();
        
        if (data.audio_url) {
            appState.storyData.audio_url = data.audio_url;
            player.src = data.audio_url;
            loading.style.display = 'none';
            playerContainer.style.display = 'block';
            player.play();
        } else {
            throw new Error('Audio generation failed');
        }
    } catch (err) {
        console.error(err);
        alert('Voice generation failed. Please try again later.');
        btn.style.display = 'flex';
        loading.style.display = 'none';
    }
}
