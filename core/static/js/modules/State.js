export class State {
    constructor() {
        this.questions = [];
        this.currentIndex = 0;
        this.score = 0;
        this.isCheckState = true;
        this.selectedOption = null;
        this.userAnswers = {}; // Store answers for review if needed
    }

    init(questions) {
        this.questions = questions;
        this.currentIndex = 0;
        this.score = 0;
        this.isCheckState = true;
        this.selectedOption = null;
    }

    get currentQuestion() {
        return this.questions[this.currentIndex];
    }

    get isFinished() {
        return this.currentIndex >= this.questions.length;
    }

    get progressPercent() {
        if (this.questions.length === 0) return 0;
        return (this.currentIndex / this.questions.length) * 100;
    }

    next() {
        this.currentIndex++;
        this.isCheckState = true; // Reset to Check state
        this.selectedOption = null;
    }

    // SRS Logic placeholder
    updateSRS(wordId, quality) {
        // ...
    }
}
