export class AudioEngine {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }

    playText(text, lang = 'ru-RU') {
        if (!text) return;
        try {
            if (this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);

                // Smart Lang Detection
                if (lang === 'auto') {
                    // Check if text contains Cyrillic
                    lang = /[а-яА-Я]/.test(text) ? 'ru-RU' : 'en-US';
                }

                utterance.lang = lang;
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }
        } catch (e) {
            console.warn("TTS Error", e);
        }
    }

    playSFX(type) {
        try {
            if (this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
            const osc = this.ctx.createOscillator();
            const gainNode = this.ctx.createGain();

            osc.connect(gainNode);
            gainNode.connect(this.ctx.destination);

            const now = this.ctx.currentTime;

            if (type === 'success' || type === 'correct') {
                // Ding sound
                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, now);
                osc.frequency.exponentialRampToValueAtTime(1000, now + 0.1);
                gainNode.gain.setValueAtTime(0.3, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
                osc.start();
                osc.stop(now + 0.5);
            } else if (type === 'pop') {
                // Bubble pop
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, now);
                osc.frequency.exponentialRampToValueAtTime(800, now + 0.05);
                gainNode.gain.setValueAtTime(0.5, now);
                gainNode.gain.linearRampToValueAtTime(0.01, now + 0.1);
                osc.start();
                osc.stop(now + 0.1);
            } else {
                // Fail sound
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(80, now);
                osc.frequency.exponentialRampToValueAtTime(30, now + 0.4);
                gainNode.gain.setValueAtTime(0.8, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
                osc.start();
                osc.stop(now + 0.4);
            }
        } catch (e) {
            console.warn("AudioContext Error", e);
        }
    }
}
