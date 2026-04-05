function renderLandingContent() {
    return `
        <div class="container text-center mt-4" style="padding-top: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🧚‍♀️✨</div>
            <h1>Turn Your Child Into the Hero of Magical Stories</h1>
            <p class="mt-2" style="font-size: 1.1rem;">AI-generated bedtime stories with voice, animation & video</p>
            
            <button class="btn-primary mt-4" onclick="navigate('form')">
                Create Your First Story <i class="fa-solid fa-arrow-right"></i>
            </button>

            <div class="mt-4" style="background: white; border-radius: var(--radius); padding: 1.5rem; text-align: left; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="font-size: 0.9rem; color: #777; margin-bottom: 10px;">LOVED BY PARENTS</div>
                <div style="display:flex; align-items:center; gap: 10px; margin-bottom: 8px;">
                    <i class="fa-solid fa-heart" style="color:#ff7675;"></i>
                    <span>Over 10,000+ stories told</span>
                </div>
                <div style="display:flex; align-items:center; gap: 10px;">
                    <i class="fa-solid fa-star" style="color:#FFE066;"></i>
                    <span>Improves imagination & sleep</span>
                </div>
            </div>
            
            <div class="mt-4" style="padding-bottom: 3rem;">
                <h3 style="margin-bottom: 1rem;">Features</h3>
                <div style="display: flex; gap: 1rem; overflow-x: auto; padding-bottom: 1rem; scroll-snap-type: x mandatory;">
                    <!-- Card 1 -->
                    <div style="min-width: 80%; background: white; padding: 1.5rem; border-radius: var(--radius); flex-shrink: 0; scroll-snap-align: center; border-bottom: 4px solid var(--primary);">
                        <i class="fa-solid fa-wand-magic-sparkles" style="font-size: 2rem; color: var(--primary); margin-bottom: 1rem;"></i>
                        <h4>Personalized</h4>
                        <p style="font-size: 0.85rem;" class="mt-2">Your child is the main character in every adventure.</p>
                    </div>
                    <!-- Card 2 -->
                    <div style="min-width: 80%; background: white; padding: 1.5rem; border-radius: var(--radius); flex-shrink: 0; scroll-snap-align: center; border-bottom: 4px solid var(--secondary);">
                        <i class="fa-solid fa-volume-high" style="font-size: 2rem; color: var(--secondary); margin-bottom: 1rem;"></i>
                        <h4>AI Voice Narration</h4>
                        <p style="font-size: 0.85rem;" class="mt-2">Soothingly read aloud by our premium artificial voices.</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}
