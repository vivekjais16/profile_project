/**
 * Vivek Jaiswal — Portfolio Frontend Interaction Script
 * Author: Vivek Jaiswal <vivekjais16@gmail.com>
 * Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Main Portfolio Mobile Navigation Toggle
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    const mobileMenuIcon = document.getElementById("mobile-menu-icon");

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const isHidden = mobileMenu.classList.contains("hidden");
            if (isHidden) {
                mobileMenu.classList.remove("hidden");
                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove("fa-bars");
                    mobileMenuIcon.classList.add("fa-xmark");
                }
            } else {
                mobileMenu.classList.add("hidden");
                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove("fa-xmark");
                    mobileMenuIcon.classList.add("fa-bars");
                }
            }
        });

        // Close when clicking any navigation link
        document.querySelectorAll(".mobile-nav-link").forEach((link) => {
            link.addEventListener("click", () => {
                mobileMenu.classList.add("hidden");
                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove("fa-xmark");
                    mobileMenuIcon.classList.add("fa-bars");
                }
            });
        });

        // Close when clicking outside header / menu drawer
        document.addEventListener("click", (e) => {
            if (!mobileMenu.classList.contains("hidden")) {
                if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    mobileMenu.classList.add("hidden");
                    if (mobileMenuIcon) {
                        mobileMenuIcon.classList.remove("fa-xmark");
                        mobileMenuIcon.classList.add("fa-bars");
                    }
                }
            }
        });
    }

    // Admin Mobile Sidebar Toggle
    const adminMobileBtn = document.getElementById("admin-mobile-menu-btn");
    const adminSidebar = document.getElementById("admin-sidebar");
    if (adminMobileBtn && adminSidebar) {
        adminMobileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            adminSidebar.classList.toggle("hidden");
        });
    }

    // 2. Skill Filter Buttons
    const filterButtons = document.querySelectorAll(".skill-filter-btn");
    const skillCards = document.querySelectorAll(".skill-category-block");

    filterButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            filterButtons.forEach((b) => {
                b.classList.remove("bg-indigo-600", "text-white");
                b.classList.add("bg-slate-800", "text-slate-300");
            });
            btn.classList.add("bg-indigo-600", "text-white");
            btn.classList.remove("bg-slate-800", "text-slate-300");

            const filterSlug = btn.getAttribute("data-category");

            skillCards.forEach((card) => {
                if (filterSlug === "all" || card.getAttribute("data-category") === filterSlug) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });

    // 3. Interactive AI Assistant / Terminal Query
    const terminalForm = document.getElementById("ai-terminal-form");
    const terminalInput = document.getElementById("ai-terminal-input");
    const terminalOutput = document.getElementById("ai-terminal-output");
    const terminalSubmitBtn = document.getElementById("ai-terminal-submit");
    const samplePrompts = document.querySelectorAll(".sample-prompt-btn");

    async function executeAIQuery(queryText) {
        if (!queryText || !queryText.trim()) return;

        // Show typing / loading state in terminal
        terminalOutput.innerHTML = `
            <div class="flex items-center space-x-2 text-emerald-400">
                <svg class="animate-spin h-4 w-4 text-emerald-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span class="font-mono text-sm">Querying Vivek's Knowledge Graph & MCP Router...</span>
            </div>
        `;

        try {
            const response = await fetch("/api/v1/agent/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: queryText }),
            });

            if (!response.ok) {
                throw new Error("Failed to process query");
            }

            const data = await response.json();

            // Render rich terminal output
            let skillsBadges = "";
            if (data.related_skills && data.related_skills.length > 0) {
                skillsBadges = data.related_skills
                    .map((s) => `<span class="px-2 py-0.5 text-xs bg-indigo-900/60 border border-indigo-500/30 text-indigo-300 rounded">${s}</span>`)
                    .join(" ");
            }

            let followupHtml = "";
            if (data.suggested_followups && data.suggested_followups.length > 0) {
                followupHtml = `
                    <div class="mt-3 pt-3 border-t border-slate-800">
                        <div class="text-xs text-slate-400 font-mono mb-2">Suggested Next Queries:</div>
                        <div class="flex flex-wrap gap-2">
                            ${data.suggested_followups
                                .map(
                                    (f) =>
                                        `<button type="button" class="terminal-followup-btn text-xs bg-slate-800 hover:bg-slate-700 text-emerald-300 border border-slate-700 px-2.5 py-1 rounded transition">${f}</button>`
                                )
                                .join("")}
                        </div>
                    </div>
                `;
            }

            let actionCardHtml = "";
            if (data.action_type === "download_resume" || data.action_url) {
                const downloadUrl = data.action_url || "/api/v1/profile/resume";
                actionCardHtml = `
                    <div class="p-3.5 mt-2 rounded-xl bg-gradient-to-r from-emerald-950/80 to-slate-900 border border-emerald-500/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg">
                        <div class="flex items-center gap-2.5">
                            <div class="p-2 rounded-lg bg-emerald-500/20 text-emerald-400 shrink-0">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                            </div>
                            <div>
                                <div class="font-bold text-white text-xs">${data.download_filename || 'Vivek_Jaiswal_Resume.pdf'}</div>
                                <div class="text-[10px] text-slate-400">Official Executive CV • 4.5+ Yrs Python, FastAPI & AI Systems</div>
                            </div>
                        </div>
                        <a href="${downloadUrl}" download="Vivek_Jaiswal_Resume.pdf" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md transition flex items-center gap-1.5 whitespace-nowrap">
                            <i class="fa-solid fa-download"></i> <span>Download PDF</span>
                        </a>
                    </div>
                `;

                // Automatically trigger download
                setTimeout(() => {
                    const downloadLink = document.createElement("a");
                    downloadLink.href = downloadUrl;
                    downloadLink.download = data.download_filename || "Vivek_Jaiswal_Resume.pdf";
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                }, 300);
            }

            terminalOutput.innerHTML = `
                <div class="space-y-3 font-mono text-sm animate-fade-in">
                    <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
                        <span class="text-emerald-400 font-semibold flex items-center gap-1.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-400"></span> Intent: ${data.matched_intent}
                        </span>
                        <span class="text-slate-500">Confidence: ${(data.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div class="text-slate-200 leading-relaxed">
                        ${data.response}
                    </div>
                    ${actionCardHtml}
                    ${skillsBadges ? `<div class="flex flex-wrap gap-1.5 items-center pt-1"><span class="text-xs text-slate-400">Related Stack:</span> ${skillsBadges}</div>` : ""}
                    ${followupHtml}
                </div>
            `;

            // Attach listeners to newly added followup buttons
            document.querySelectorAll(".terminal-followup-btn").forEach((btn) => {
                btn.addEventListener("click", () => {
                    const text = btn.textContent.trim();
                    terminalInput.value = text;
                    executeAIQuery(text);
                });
            });
        } catch (err) {
            terminalOutput.innerHTML = `
                <div class="text-rose-400 font-mono text-sm">
                    ⚠️ Error executing agent query: ${err.message}. Please check connection or try again.
                </div>
            `;
        }
    }

    if (terminalForm && terminalInput) {
        terminalForm.addEventListener("submit", (e) => {
            e.preventDefault();
            executeAIQuery(terminalInput.value);
        });
    }

    samplePrompts.forEach((btn) => {
        btn.addEventListener("click", () => {
            const promptText = btn.getAttribute("data-prompt") || btn.textContent.trim();
            terminalInput.value = promptText;
            executeAIQuery(promptText);
        });
    });

    // 4. Contact Form Submission
    const contactForm = document.getElementById("contact-form");
    const contactFeedback = document.getElementById("contact-feedback");
    const contactSubmitBtn = document.getElementById("contact-submit-btn");

    if (contactForm) {
        contactForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const senderName = document.getElementById("sender_name").value.trim();
            const senderEmail = document.getElementById("sender_email").value.trim();
            const subject = document.getElementById("subject").value.trim();
            const message = document.getElementById("message").value.trim();

            if (!senderName || !senderEmail || !subject || !message) {
                showToast("Please fill in all required fields.", "error");
                return;
            }

            contactSubmitBtn.disabled = true;
            contactSubmitBtn.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg> Sending message...
            `;

            try {
                const response = await fetch("/api/v1/contact", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        sender_name: senderName,
                        sender_email: senderEmail,
                        subject: subject,
                        message: message,
                    }),
                });

                const resData = await response.json();

                if (response.ok && resData.success) {
                    showToast(resData.message, "success");
                    contactForm.reset();
                } else {
                    let detailMsg = "Please verify your input.";
                    if (Array.isArray(resData.detail)) {
                        detailMsg = resData.detail.map(err => {
                            const rawField = err.loc ? err.loc[err.loc.length - 1] : 'field';
                            const fieldName = rawField.replace('sender_', '').replace('_', ' ');
                            return `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)}: ${err.msg}`;
                        }).join(" • ");
                    } else if (typeof resData.detail === 'string') {
                        detailMsg = resData.detail;
                    }
                    showToast(detailMsg, "error");
                }
            } catch (err) {
                showToast("Network error: unable to send message right now.", "error");
            } finally {
                contactSubmitBtn.disabled = false;
                contactSubmitBtn.innerHTML = `
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                    </svg> Send Message
                `;
            }
        });
    }

    // 5. Toast Notification System
    function showToast(message, type = "success") {
        let container = document.getElementById("toast-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            container.className = "fixed bottom-5 right-5 z-50 flex flex-col space-y-2";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        const bgColor = type === "success" ? "bg-emerald-950 border-emerald-500 text-emerald-200" : "bg-rose-950 border-rose-500 text-rose-200";
        toast.className = `border px-4 py-3 rounded-lg shadow-xl text-sm flex items-center space-x-2 transition-all duration-300 transform translate-y-2 ${bgColor}`;
        toast.innerHTML = `
            <span>${type === "success" ? "✓" : "⚠️"}</span>
            <span>${message}</span>
        `;

        container.appendChild(toast);
        setTimeout(() => toast.classList.remove("translate-y-2"), 10);
        setTimeout(() => {
            toast.classList.add("opacity-0", "translate-y-2");
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});

// =========================================================================
// Global Carousel & Modal Handlers (Netflix/Linear Style Showcase)
// =========================================================================

/**
 * Smoothly scroll horizontal card containers
 */
function scrollRow(containerId, direction) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const scrollAmount = 360;
    if (direction === "left") {
        container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    } else {
        container.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
}

/**
 * Open Project Deep Dive Modal Dialog
 */
function openProjectModal(index) {
    if (typeof SHOWCASE_PROJECTS === "undefined" || !SHOWCASE_PROJECTS[index]) return;
    const p = SHOWCASE_PROJECTS[index];
    const modal = document.getElementById("showcase-modal");
    if (!modal) return;

    // Badge & Category
    const badgeEl = document.getElementById("modal-badge");
    const catEl = document.getElementById("modal-category");
    if (badgeEl) badgeEl.textContent = p.badge || "Featured Architecture";
    if (catEl) catEl.innerHTML = `<i class="fa-solid fa-microchip mr-1"></i> ${p.category || 'Platform'}`;

    // Title & Tagline
    const titleEl = document.getElementById("modal-title");
    const taglineEl = document.getElementById("modal-tagline");
    if (titleEl) titleEl.textContent = p.title;
    if (taglineEl) taglineEl.textContent = p.tagline || "";

    // Architecture Summary
    const descEl = document.getElementById("modal-description");
    if (descEl) descEl.textContent = p.architecture_summary || "";

    // Key Features
    const featSection = document.getElementById("modal-features-section");
    const featList = document.getElementById("modal-features");
    if (featSection && featList) {
        if (p.key_features && p.key_features.trim()) {
            featSection.style.display = "block";
            const items = p.key_features.split(/\r?\n|;/).map(s => s.trim()).filter(Boolean);
            featList.innerHTML = items.map(item => `
                <li class="flex items-start gap-2">
                    <i class="fa-solid fa-check text-emerald-400 mt-1 shrink-0 text-xs"></i>
                    <span>${item.replace(/^[•\-\*]\s*/, "")}</span>
                </li>
            `).join("");
        } else {
            featSection.style.display = "none";
            featList.innerHTML = "";
        }
    }

    // Tech Stack Tags
    const techSection = document.getElementById("modal-tech-section");
    const techTags = document.getElementById("modal-tech-tags");
    if (techSection && techTags) {
        if (p.tech_stack && p.tech_stack.trim()) {
            techSection.style.display = "block";
            const tags = p.tech_stack.split(",").map(s => s.trim()).filter(Boolean);
            techTags.innerHTML = tags.map(tag => `
                <span class="px-2.5 py-1 text-xs font-mono rounded bg-slate-800 text-indigo-200 border border-slate-700/80">
                    ${tag}
                </span>
            `).join("");
        } else {
            techSection.style.display = "none";
            techTags.innerHTML = "";
        }
    }

    // Action Links
    const githubBtn = document.getElementById("modal-github-btn");
    const liveBtn = document.getElementById("modal-live-btn");
    if (githubBtn) {
        if (p.github_url && p.github_url.trim()) {
            githubBtn.href = p.github_url;
            githubBtn.style.display = "inline-flex";
        } else {
            githubBtn.style.display = "none";
        }
    }
    if (liveBtn) {
        if (p.live_demo_url && p.live_demo_url.trim()) {
            liveBtn.href = p.live_demo_url;
            liveBtn.style.display = "inline-flex";
        } else {
            liveBtn.style.display = "none";
        }
    }

    // Reveal modal
    modal.classList.remove("hidden");
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
}

/**
 * Open Experience Deep Dive Modal Dialog
 */
function openExperienceModal(index) {
    if (typeof SHOWCASE_EXPERIENCES === "undefined" || !SHOWCASE_EXPERIENCES[index]) return;
    const e = SHOWCASE_EXPERIENCES[index];
    const modal = document.getElementById("showcase-modal");
    if (!modal) return;

    // Badge & Category
    const badgeEl = document.getElementById("modal-badge");
    const catEl = document.getElementById("modal-category");
    if (badgeEl) badgeEl.textContent = e.is_current ? "CURRENT ROLE" : "CAREER MILESTONE";
    if (catEl) catEl.innerHTML = `<i class="fa-solid fa-briefcase mr-1"></i> ${e.company}`;

    // Title & Tagline
    const titleEl = document.getElementById("modal-title");
    const taglineEl = document.getElementById("modal-tagline");
    if (titleEl) titleEl.textContent = e.title;
    if (taglineEl) taglineEl.textContent = `${e.dates} • ${e.location}`;

    // Description / Summary
    const descEl = document.getElementById("modal-description");
    if (descEl) descEl.textContent = `Production engineering milestones, system reliability, and microservices impact at ${e.company}.`;

    // Highlights
    const featSection = document.getElementById("modal-features-section");
    const featList = document.getElementById("modal-features");
    if (featSection && featList) {
        if (e.highlights && e.highlights.length > 0) {
            featSection.style.display = "block";
            featList.innerHTML = e.highlights.map(h => `
                <li class="flex items-start gap-2">
                    <i class="fa-solid fa-arrow-right text-cyan-400 mt-1 shrink-0 text-xs"></i>
                    <span>${h}</span>
                </li>
            `).join("");
        } else {
            featSection.style.display = "none";
            featList.innerHTML = "";
        }
    }

    // Tech Stack Tags
    const techSection = document.getElementById("modal-tech-section");
    const techTags = document.getElementById("modal-tech-tags");
    if (techSection && techTags) {
        if (e.tech_stack && e.tech_stack.trim()) {
            techSection.style.display = "block";
            const tags = e.tech_stack.split(",").map(s => s.trim()).filter(Boolean);
            techTags.innerHTML = tags.map(tag => `
                <span class="px-2.5 py-1 text-xs font-mono rounded bg-slate-800 text-cyan-200 border border-slate-700/80">
                    ${tag}
                </span>
            `).join("");
        } else {
            techSection.style.display = "none";
            techTags.innerHTML = "";
        }
    }

    // Hide Project Buttons for Experience Modal
    const githubBtn = document.getElementById("modal-github-btn");
    const liveBtn = document.getElementById("modal-live-btn");
    if (githubBtn) githubBtn.style.display = "none";
    if (liveBtn) liveBtn.style.display = "none";

    // Reveal modal
    modal.classList.remove("hidden");
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
}

/**
 * Close Modal Dialog
 */
function closeShowcaseModal(event) {
    if (event && event.target && event.target.id !== "showcase-modal" && !event.target.closest(".modal-close-btn") && !event.target.closest("#modal-close-action-btn")) {
        return;
    }
    const modal = document.getElementById("showcase-modal");
    if (modal) {
        modal.classList.remove("active");
        modal.classList.add("hidden");
        document.body.style.overflow = "";
    }
}

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        const modal = document.getElementById("showcase-modal");
        if (modal && (modal.classList.contains("active") || !modal.classList.contains("hidden"))) {
            closeShowcaseModal();
        }
    }
});

// Explicitly bind to window for inline onclick handlers
window.scrollRow = scrollRow;
window.openProjectModal = openProjectModal;
window.openExperienceModal = openExperienceModal;
window.closeShowcaseModal = closeShowcaseModal;

