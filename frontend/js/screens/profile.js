function renderProfileContent() {
    return `
        <div class="container mt-4" style="padding-bottom: 5rem;">
            <h2>Profile 👤</h2>
            
            <div class="mt-4" style="text-align: center;">
                <div style="width: 100px; height: 100px; border-radius: 50%; background: #eee; margin: 0 auto; display:flex; align-items:center; justify-content:center; font-size: 3rem; color: #ccc;">
                    <i class="fa-solid fa-user"></i>
                </div>
                <h3 class="mt-2 text-primary">Story Parent</h3>
                <p style="color: #888;">parent@example.com</p>
            </div>

            <div class="mt-4" style="background: white; padding: 1.5rem; border-radius: var(--radius); box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>Current Plan</h4>
                    <span style="background: var(--accent); padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; color: #333;">Free Trial</span>
                </div>
                <p style="font-size: 0.9rem; margin-top: 10px; color: #666;">You have 2 stories remaining.</p>
                <button class="btn-primary mt-4" style="font-size: 0.95rem; padding: 10px;">
                    Upgrade to Premium <i class="fa-solid fa-star" style="margin-left:5px; color:#FFE066;"></i>
                </button>
            </div>
            
            <div class="mt-4">
               <button style="width: 100%; padding: 15px; background: transparent; border: 1px solid #ddd; border-radius: var(--radius); cursor: pointer; color: #ff7675; font-weight: 500;">
                   Log Out
               </button>
            </div>
        </div>
    `;
}
