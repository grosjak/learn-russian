import { State } from './State.js';
import { AudioEngine } from './AudioEngine.js';

export class UI {
    constructor(state, audio, grammar, containers) {
        this.state = state;
        this.audio = audio;
        this.grammar = grammar;
        this.containers = containers; // { area, footer, progress }

        // Bind methods
        this.render = this.render.bind(this);
        this.handleCheck = this.handleCheck.bind(this);
        this.handleKeyDown = this.handleKeyDown.bind(this);
    }

    init() {
        // Initial setup
        const checkBtn = document.getElementById('checkBtn');
        if (checkBtn) {
            checkBtn.onclick = this.handleCheck;
        }
        this.updateProgress();
        this.enablePhoneticSandbox();
    }

    enablePhoneticSandbox() {
        document.addEventListener('keydown', this.handleKeyDown);
    }

    handleKeyDown(e) {
        // Only active if alphabet grid or special mode
        const q = this.state.currentQuestion;
        if (!q || q.type !== 'alphabet_grid') return;

        // Latin A-Z only
        if (/^[a-zA-Z]$/.test(e.key)) {
            const cyr = this.grammar.getCyrillic(e.key);
            if (cyr) {
                // Visualize
                this.showSandboxOverlay(cyr);
            }
        }
    }

    showSandboxOverlay(char) {
        let overlay = document.getElementById('sandbox-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'sandbox-overlay';
            overlay.style.position = 'fixed';
            overlay.style.top = '50%';
            overlay.style.left = '50%';
            overlay.style.transform = 'translate(-50%, -50%)';
            overlay.style.fontSize = '10rem';
            overlay.style.color = 'white';
            overlay.style.background = 'rgba(0,0,0,0.8)';
            overlay.style.padding = '50px';
            overlay.style.borderRadius = '20px';
            overlay.style.zIndex = '2000';
            overlay.style.pointerEvents = 'none';
            document.body.appendChild(overlay);
        }

        const friendship = this.grammar.getFriendshipStatus(char);
        const color = friendship === 'true' ? '#58CC02' : (friendship === 'false' ? '#FF4B4B' : '#ffffff');
        const label = friendship === 'true' ? 'Vrai Ami! 😊' : (friendship === 'false' ? 'Faux Ami! 😈' : 'Nouveau');

        overlay.innerHTML = `
            <div style="color: ${color}">${char.toUpperCase()}</div>
            <div style="font-size: 2rem; margin-top: 20px; color: #ddd;">${label}</div>
        `;
        overlay.style.opacity = '1';

        // Fade out
        clearTimeout(this.overlayTimeout);
        this.overlayTimeout = setTimeout(() => {
            overlay.style.opacity = '0';
        }, 1500);
    }

    updateProgress() {
        if (!this.containers.progress) return;
        this.containers.progress.style.width = `${this.state.progressPercent}%`;
    }

    render() {
        if (this.state.isFinished) {
            this.showCompletion();
            return;
        }

        const q = this.state.currentQuestion;
        this.updateProgress();

        // Reset UI State
        this.containers.area.innerHTML = '';
        this.resetFooter();

        // Dispatch based on type
        switch (q.type) {
            case 'intro':
            case 'intro_word':
                this.renderIntro(q);
                break;
            case 'alphabet_grid':
                this.renderAlphabetGrid(q);
                break;
            case 'select_sound':
            case 'select_char':
            case 'select_trans':
                this.renderSelect(q);
                break;
            case 'select_translation':
            case 'select_word':
            case 'listen_and_select':
                this.renderSelectText(q);
                break;
            case 'input_text':
                this.renderInput(q);
                break;
            case 'construct_sentence':
                this.renderConstruct(q);
                break;
            case 'suffix_snap':
                this.renderSuffixSnap(q);
                break;
            default:
                this.containers.area.innerHTML = `<div>Unknown Type: ${q.type}</div>`;
        }
    }

    // ...

    renderSuffixSnap(q) {
        this.containers.area.innerHTML = `
            <h2>${q.prompt || 'Complétez le mot'}</h2>
            <div style="text-align: center; margin: 30px 0;">
                <div class="root-display">${q.root}</div>
                <div id="target-slot" class="suffix-slot"></div>
            </div>
            
            <div class="suffix-container">
                ${q.options.map(opt => `
                    <button class="suffix-block" data-val="${opt}">${opt}</button>
                `).join('')}
            </div>
        `;

        const slot = document.getElementById('target-slot');
        const blocks = this.containers.area.querySelectorAll('.suffix-block');

        blocks.forEach(btn => {
            btn.onclick = () => {
                if (!this.state.isCheckState) return;

                // Visual selection
                blocks.forEach(b => {
                    b.style.transform = 'none';
                    b.style.boxShadow = ''; // Reset neumorphism
                    b.classList.remove('selected');
                });

                btn.classList.add('selected');
                btn.style.boxShadow = 'inset 4px 4px 8px #bebebe, inset -4px -4px 8px #ffffff'; // Pressed state

                // Move text to slot? Or just keep selected?
                // Plan says "Snap". Let's update slot text.
                slot.innerText = btn.dataset.val;
                slot.style.borderBottomStyle = 'solid';
                slot.style.borderColor = '#1CB0F6';

                this.state.selectedOption = btn.dataset.val;

                const checkBtn = document.getElementById('checkBtn');
                if (checkBtn) checkBtn.disabled = false;
            };
        });
    }

    resetFooter() {
        const checkBtn = document.getElementById('checkBtn');
        const footer = this.containers.footer;

        if (checkBtn) {
            checkBtn.disabled = true;
            checkBtn.innerText = 'Vérifier';
            checkBtn.className = 'btn-primary';
            checkBtn.style = '';
            checkBtn.style.display = 'block';
            checkBtn.onclick = this.handleCheck; // Re-bind
        }

        if (footer) {
            footer.className = 'check-footer';
            footer.style = '';
            // Restore default if it was wiped
            if (!footer.contains(checkBtn) && checkBtn) {
                footer.innerHTML = '';
                footer.appendChild(checkBtn);
            }
        }
    }

    handleCheck() {
        if (!this.state.isCheckState) {
            // Continue
            this.state.next();
            this.render();
            return;
        }

        const q = this.state.currentQuestion;

        // Validation Dispatch
        if (['intro', 'intro_word', 'alphabet_grid'].includes(q.type)) {
            // Just acknowledge
            this.state.next();
            this.render();
        } else if (q.type === 'input_text') {
            this.validateInput(q);
        } else if (q.type === 'construct_sentence') {
            this.validateConstruct(q);
        } else if (q.type === 'suffix_snap') {
            this.validateSuffixSnap(q);
        } else {
            this.validateSelection(q);
        }
    }

    // --- Renderers ---

    // ... (render methods)

    // --- Validation ---

    validateSuffixSnap(q) {
        const correct = q.correct;
        const selected = this.state.selectedOption;
        const isCorrect = (selected === correct);

        // Visual Feedback on Suffix Blocks
        const blocks = this.containers.area.querySelectorAll('.suffix-block');
        blocks.forEach(btn => {
            const val = btn.dataset.val;

            // Apply Case Color if known (e.g. q.case = 'acc')
            // If correct button: show its case color
            if (val === correct) {
                if (q.case) btn.classList.add(`case-${q.case}`);
                btn.style.backgroundColor = isCorrect ? '#d7ffb8' : '#e0e0e0'; // Light green if correct ref
                btn.style.borderColor = isCorrect ? '#58CC02' : '#e0e0e0';
                if (!isCorrect) btn.classList.add('correct'); // Just in case we want generic green
            }

            // If wrong button selected
            if (val === selected && !isCorrect) {
                btn.style.backgroundColor = '#ffdfe0';
                btn.classList.add('wrong');
            }
        });

        this.showFeedbackFooter(isCorrect, correct, q.grammar_rule || (q.case ? `Cas : ${q.case}` : ''));
        this.audio.playSFX(isCorrect ? 'success' : 'error');
        this.state.isCheckState = false;
    }

    renderIntro(q) {
        const btn = document.getElementById('checkBtn');
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Compris";
        }

        if (q.type === 'intro') {
            this.containers.area.innerHTML = `
                <div style="text-align: center;">
                    <h2>Nouvelle Lettre !</h2>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <div class="big-char" style="margin: 30px 0; color: #58CC02;">${q.char}</div>
                        <button class="audio-btn" data-text="${q.char}">🔊</button>
                    </div>
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">Nom : <b>${q.name}</b></div>
                    <div style="font-size: 1.5rem; color: #777;">Son : /${q.trans}/</div>
                    <div style="margin-top: 20px; font-style: italic;">"${q.desc}"</div>
                </div>
            `;
        } else {
            this.containers.area.innerHTML = `
                <div style="text-align: center;">
                    <h2>Nouveau Mot !</h2>
                    <div style="font-size: 2rem; margin: 20px 0; color: #58CC02; font-weight: bold;">${q.word}</div>
                    <button class="audio-btn" data-text="${q.word}" style="font-size: 2rem; margin-bottom: 20px;">🔊</button>
                    <div style="font-size: 1.5rem; color: #555;">${q.translation}</div>
                    <div style="margin-top: 10px; color: #aaa;">(${q.category === 'verb' ? 'Verbe' : 'Mot'})</div>
                    ${q.example ? `<div style="margin-top: 20px; font-style: italic; color: #1CB0F6; font-size: 1.2rem;">"${q.example}"</div>` : ''}
                </div>
            `;
        }
        this.bindAudio();
        this.audio.playText(q.char || q.word);
    }

    renderAlphabetGrid(q) {
        const btn = document.getElementById('checkBtn');
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Apprendre";
        }
        this.containers.area.innerHTML = `
            <div style="text-align: center;">
                <h2>Alphabet Russe</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(60px, 1fr)); gap: 10px; max-width: 600px; margin: 0 auto;">
                    ${q.letters.map(l => `
                        <div class="grid-char-item" data-text="${l.char}" style="background: #2b2b2b; padding: 10px; border-radius: 10px; border: 2px solid #373737; cursor: pointer;">
                            <div style="font-size: 1.5rem; color: #58CC02; font-weight: bold;">${l.char}</div>
                            <div style="font-size: 0.9rem; color: #aaa;">/${l.trans}/</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        // Add listeners manually since we are in module
        this.containers.area.querySelectorAll('.grid-char-item').forEach(el => {
            el.onclick = () => this.audio.playText(el.dataset.text);
        });
    }

    renderSelect(q) {
        // ... (Similar logic to renderSelectSound/Char)
        // Check if sound or char
        const isSound = q.type === 'select_sound';
        const main = isSound ? q.main_char : `/${q.main_sound}/`;

        this.containers.area.innerHTML = `
            <h2>${q.prompt}</h2>
             <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
                ${isSound ? `<button class="audio-btn" data-text="${q.main_char}" style="font-size: 3rem; margin-right: 15px;">🔊</button>` : ''}
                <div class="${isSound ? 'big-char' : ''}" style="${!isSound ? 'font-size: 3rem; color: #1CB0F6;' : ''}">${main}</div>
            </div>
            <div class="options-grid">
                ${q.options.map(opt => `<div class="option-btn" data-val="${opt}">${opt}</div>`).join('')}
            </div>
        `;

        this.bindOptions();
        this.bindAudio();
        if (isSound) setTimeout(() => this.audio.playText(q.main_char), 500);
    }

    renderSelectText(q) {
        // Translation or Word or Listen
        const isListen = q.type === 'listen_and_select';

        this.containers.area.innerHTML = `
            <h2>${q.prompt}</h2>
             <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    ${q.main_word && !isListen ? `<div class="big-char" style="font-size: 2.5rem;">${q.main_word}</div>` : ''}
                    ${(q.main_word && !isListen) || isListen ? `<button class="audio-btn" data-text="${q.main_word || q.reveal_word}" style="font-size: ${isListen ? '4rem' : '2rem'};">🔊</button>` : ''}
                </div>
                ${q.example ? `<div style="margin-top: 10px; font-style: italic; color: #888;">"${q.example}"</div>` : ''}
            </div>
            <div class="options-grid">
                ${q.options.map(opt => `<div class="option-btn" data-val="${opt}">${opt}</div>`).join('')}
            </div>
        `;

        this.bindOptions();
        this.bindAudio();
        if ((q.type === 'select_translation' || isListen) && (q.main_word || q.reveal_word)) {
            setTimeout(() => this.audio.playText(q.main_word || q.reveal_word), 500);
        }
    }

    renderInput(q) {
        // ... Input logic
        this.containers.area.innerHTML = `
            <div style="text-align: center; max-width: 600px; margin: 0 auto;">
                <h2 style="margin-bottom: 1rem;">${q.prompt}</h2>
                 <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 2rem;">
                    <!-- Hint Btn if not English -->
                </div>
                
                ${q.category === 'verb' ? '<div id="aspect-slider-area" style="margin-bottom: 20px;"></div>' : ''}

                <textarea id="userAnswer" class="user-input" placeholder="Tapez votre réponse..." rows="2"></textarea>
            </div>
        `;

        if (q.category === 'verb') {
            this.renderAspectSlider(document.getElementById('aspect-slider-area'));
        }

        const input = document.getElementById('userAnswer');
        input.oninput = (e) => {
            const btn = document.getElementById('checkBtn');
            btn.disabled = e.target.value.trim().length === 0;
            if (!btn.disabled) {
                btn.style.backgroundColor = '#58CC02';
                btn.style.color = 'white';
            } else {
                btn.style.backgroundColor = '';
                btn.style.color = '';
            }
        };
        input.onkeypress = (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('checkBtn').click();
            }
        };
        input.focus();
    }

    renderAspectSlider(container) {
        container.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; color: #aaa; font-weight: bold;">
                <span>Imperfectif</span>
                <input type="range" id="aspectSlider" min="0" max="1" step="1" value="0" style="width: 60px; accent-color: #1CB0F6;">
                <span>Perfectif</span>
            </div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">(Glissez pour changer l'aspect)</div>
        `;
    }

    renderConstruct(q) {
        this.containers.area.innerHTML = `
            <div class="question-card fade-in">
                 <div class="intro-content">
                    <h2 class="question-prompt" style="text-align:center;">${q.prompt}</h2>
                 </div>
                 <div class="bubble-container">
                    <div id="drop-zone" class="drop-zone"></div>
                    <div id="word-bank" class="word-bank"></div>
                 </div>
            </div>
        `;

        const dropZone = document.getElementById('drop-zone');
        const wordBank = document.getElementById('word-bank');

        // Populate Bank
        q.options.forEach((word, index) => {
            const btn = document.createElement('div');
            btn.className = 'bubble-word fade-in';
            btn.textContent = word;
            btn.onclick = () => {
                this.audio.playSFX('pop');
                if (btn.parentNode === wordBank) {
                    wordBank.removeChild(btn);
                    dropZone.appendChild(btn);
                } else {
                    dropZone.removeChild(btn);
                    wordBank.appendChild(btn);
                }

                const hasWords = dropZone.children.length > 0;
                const checkBtn = document.getElementById('checkBtn');
                checkBtn.disabled = !hasWords;
                if (hasWords) {
                    checkBtn.style.backgroundColor = '#58CC02';
                    checkBtn.style.color = 'white';
                } else {
                    checkBtn.style.backgroundColor = '';
                    checkBtn.style.color = '';
                }
            };
            wordBank.appendChild(btn);
        });
    }

    // --- Binders ---
    bindOptions() {
        this.containers.area.querySelectorAll('.option-btn').forEach(btn => {
            btn.onclick = () => {
                if (!this.state.isCheckState) return;
                this.containers.area.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.state.selectedOption = btn.dataset.val;

                const checkBtn = document.getElementById('checkBtn');
                if (checkBtn) checkBtn.disabled = false;
            }
        });
    }

    bindAudio() {
        this.containers.area.querySelectorAll('.audio-btn').forEach(btn => {
            btn.onclick = (e) => {
                e.preventDefault();
                this.audio.playText(btn.dataset.text);
            };
        });
    }

    // --- Validation ---

    validateSelection(q) {
        const correct = q.correct;
        const selected = this.state.selectedOption;
        const isCorrect = (selected === correct);

        // Visual Feedback
        this.containers.area.querySelectorAll('.option-btn').forEach(btn => {
            const val = btn.dataset.val;
            if (val === correct) btn.classList.add('correct');
            if (val === selected && !isCorrect) btn.classList.add('wrong');
        });

        this.showFeedbackFooter(isCorrect, correct);
        this.audio.playSFX(isCorrect ? 'success' : 'error');
        this.state.isCheckState = false;
    }

    validateInput(q) {
        const input = document.getElementById('userAnswer');
        const userText = input.value.trim();
        let correctAspect = true;

        // Aspect Check
        if (q.category === 'verb') {
            const slider = document.getElementById('aspectSlider');
            const val = slider.value; // 0 or 1
            const userAspect = val === '1' ? 'perf' : 'imp';
            // Assume q.aspect is provided by backend
            if (q.aspect && q.aspect !== userAspect && q.aspect !== 'none') {
                correctAspect = false;
            }
        }

        const btn = document.getElementById('checkBtn');
        btn.disabled = true;
        btn.innerText = '...';

        fetch('/api/validate/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                word_id: q.id,
                user_input: userText,
                aspect_check: correctAspect
            })
        })
            .then(r => r.json())
            .then(data => {
                // Override correctness if aspect is wrong
                let isCorrect = data.is_correct;
                let detail = data.diff_html;

                if (isCorrect && !correctAspect) {
                    isCorrect = false;
                    detail = `Aspect incorrect ! (Attendu : ${q.aspect === 'perf' ? 'Perfectif' : 'Imperfectif'})`;
                }

                this.showFeedbackFooter(isCorrect, data.correct_answer, detail);
                this.audio.playSFX(isCorrect ? 'success' : 'error');
                this.state.isCheckState = false;
            });
    }

    validateConstruct(q) {
        const dropZone = document.getElementById('drop-zone');
        const userSentence = Array.from(dropZone.children).map(b => b.textContent).join(' ');

        // Normalize
        const normUser = userSentence.trim().toLowerCase().replace(/[.,!?;]/g, '');
        const normCorrect = q.correct_sentence.trim().toLowerCase().replace(/[.,!?;]/g, '');

        const isCorrect = (normUser === normCorrect);
        this.showFeedbackFooter(isCorrect, q.correct_sentence);
        this.audio.playSFX(isCorrect ? 'success' : 'error');
        this.state.isCheckState = false;
    }

    showFeedbackFooter(isCorrect, correctAnswer, detail) {
        const footer = this.containers.footer;
        const checkBtn = document.getElementById('checkBtn');

        const color = isCorrect ? '#d7ffb8' : '#ffdfe0';
        footer.style.backgroundColor = color;

        // Remove checkBtn for now, replace with feedback content?
        // Or keep CheckBtn but rename it "Continue"
        // Logic used in original file: rename button.

        if (checkBtn) {
            checkBtn.innerText = 'Continuer';
            checkBtn.disabled = false;
            checkBtn.style.backgroundColor = isCorrect ? '#58CC02' : '#FF4B4B';
            checkBtn.style.color = 'white';
        }

        // We can inject extra info details before the button ??
        // For simplicity, we stick to button text change for now, 
        // BUT user wanted "Neumorphic design".
        // Let's create a new feedback container above logic if needed.

        // Using the logic from previous file: replace footer innerHTML
        footer.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%; margin-bottom:10px;">
                <div style="display:flex; gap:10px; align-items:center;">
                    <div style="font-size:2rem;">${isCorrect ? '🎉' : '❌'}</div>
                    <div>
                        <h3 style="margin:0; color:${isCorrect ? '#58CC02' : '#FF4B4B'}">${isCorrect ? 'Excellent !' : 'Oups...'}</h3>
                        ${!isCorrect ? `<div style="color:#555;">Réponse : <b>${correctAnswer}</b></div>` : ''}
                        ${detail ? `<div style="font-size:0.8rem;">${detail}</div>` : ''}
                    </div>
                </div>
                 <button class="audio-btn-footer" style="padding:10px;">🔊</button>
            </div>
         `;
        // Re-add continue button
        const continueBtn = document.createElement('button');
        continueBtn.className = 'btn-primary';
        continueBtn.innerText = 'Continuer';
        continueBtn.style.backgroundColor = isCorrect ? '#58CC02' : '#FF4B4B';
        continueBtn.style.color = 'white';
        continueBtn.onclick = this.handleCheck;

        footer.appendChild(continueBtn);

        footer.querySelector('.audio-btn-footer').onclick = () => this.audio.playText(correctAnswer);

        if (isCorrect) setTimeout(() => this.audio.playText(correctAnswer), 300);
    }

    showCompletion() {
        this.containers.area.innerHTML = `
            <div style="text-align: center; margin-top: 50px;">
                <div style="font-size: 5rem;">🎉</div>
                <h2>Leçon terminée !</h2>
                <button class="btn-primary" onclick="window.location.href='/'">Menu Principal</button>
            </div>
        `;
        this.containers.footer.innerHTML = ''; // Clear footer
        if (this.containers.progress) this.containers.progress.style.width = '100%';
        this.audio.playSFX('success');
    }
}
