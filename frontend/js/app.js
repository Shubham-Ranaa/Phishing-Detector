// app.js - Main application logic and UI bindings

document.addEventListener('DOMContentLoaded', () => {
    
    // Background Particles
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = Math.random() * 3 + 'px';
            particle.style.height = particle.style.width;
            particle.style.background = 'rgba(34, 211, 238, 0.5)';
            particle.style.borderRadius = '50%';
            particle.style.top = Math.random() * 100 + 'vh';
            particle.style.left = Math.random() * 100 + 'vw';
            particle.style.animation = `fadeIn ${Math.random() * 3 + 2}s infinite alternate`;
            particlesContainer.appendChild(particle);
        }
    }
    
    // Mobile Menu
    const mobileMenuBtn = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.background = 'rgba(10, 14, 23, 0.95)';
                navLinks.style.padding = '24px';
                navLinks.style.borderBottom = '1px solid var(--border-color)';
            }
        });
    }
    
    // Tab Switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => {
                c.classList.remove('active');
            });
            
            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });
    
    // Clear Input Buttons
    const setupClearBtn = (inputId, clearBtnId) => {
        const input = document.getElementById(inputId);
        const clearBtn = document.getElementById(clearBtnId);
        
        if (input && clearBtn) {
            input.addEventListener('input', () => {
                clearBtn.style.display = input.value.length > 0 ? 'block' : 'none';
            });
            
            clearBtn.addEventListener('click', () => {
                input.value = '';
                clearBtn.style.display = 'none';
                input.focus();
            });
        }
    };
    
    setupClearBtn('url-input', 'clear-url');
    setupClearBtn('message-input', 'clear-message');
    
    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Check saved theme
    const savedTheme = localStorage.getItem('phishguard_theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        themeIcon.classList.remove('bx-sun');
        themeIcon.classList.add('bx-moon');
    }
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            
            // Update icon
            if (isLight) {
                themeIcon.classList.remove('bx-sun');
                themeIcon.classList.add('bx-moon');
                localStorage.setItem('phishguard_theme', 'light');
            } else {
                themeIcon.classList.remove('bx-moon');
                themeIcon.classList.add('bx-sun');
                localStorage.setItem('phishguard_theme', 'dark');
            }
        });
    }

    // Navigation Routing
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page-view');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from nav links
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // Hide all pages
            pages.forEach(page => {
                page.style.display = 'none';
                page.classList.remove('active-page');
            });
            
            // Show target page
            const targetId = item.getAttribute('data-page');
            const targetPage = document.getElementById(targetId);
            if (targetPage) {
                targetPage.style.display = 'block';
                // Trigger reflow for animation
                void targetPage.offsetWidth;
                targetPage.classList.add('active-page');
                targetPage.style.animation = 'fadeIn 0.4s ease forwards';
                
                // If it's the history page, make sure to re-render to get latest
                if (targetId === 'page-history' && window.History) {
                    window.History.render();
                }
            }
            
            // Close mobile menu if open
            if (window.innerWidth <= 768 && navLinks) {
                navLinks.style.display = 'none';
            }
        });
    });

    // Update active nav link based on scroll
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section[id]');
        const scrollY = window.pageYOffset;
        
        // This is a simple implementation, can be expanded
    });
});
