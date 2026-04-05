function renderLoadingContent() {
    return `
        <div class="container text-center" style="display:flex; flex-direction:column; justify-content:center; min-height: 80vh;">
            <div style="font-size: 6rem; margin-bottom: 2rem;" class="pulse-anim">⏳</div>
            <h2 id="loadingMsg">Writing your magical story ✍️</h2>
            <div style="width: 100%; height: 8px; background: #E0E0E0; border-radius: 4px; margin-top: 2rem; overflow: hidden; position: relative;">
                <div style="width: 50%; height: 100%; background: var(--primary); position: absolute; left: -50%; animation: loadBar 2s infinite linear; border-radius: 4px;"></div>
            </div>
            <p class="mt-4" style="color: #888; font-size: 0.9rem;">This usually takes a minute or two...</p>
        </div>
        <style>
            @keyframes loadBar {
                0% { left: -50%; width: 50%; }
                100% { left: 100%; width: 50%; }
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            .pulse-anim { animation: pulse 2s infinite; }
        </style>
    `;
}

function mount_loading() {
    const messages = [
        "Writing your magical story ✍️",
        "Adding voice narration 🎧",
        "Creating animated scenes 🎬",
        "Adding the finishing touches ✨"
    ];
    let step = 0;
    
    // Cycle text every 8 seconds
    window.loadingInterval = setInterval(() => {
        step = (step + 1) % messages.length;
        const msgEl = document.getElementById('loadingMsg');
        if (msgEl) {
            msgEl.innerText = messages[step];
        } else {
            clearInterval(window.loadingInterval);
        }
    }, 8000);
}
