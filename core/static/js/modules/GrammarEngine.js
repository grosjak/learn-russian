export class GrammarEngine {
    constructor() {
        this.caseColors = {
            nom: '#FFFFFF',
            acc: '#3498db',
            gen: '#f1c40f',
            dat: '#2ecc71',
            inst: '#9b59b6',
            prep: '#e67e22'
        };

        this.translitMap = {
            'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е',
            'yo': 'ё', 'zh': 'ж', 'z': 'з', 'i': 'и', 'j': 'й', 'k': 'к',
            'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р',
            's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц',
            'ch': 'ч', 'sh': 'ш', 'sch': 'щ', 'y': 'ы', 'yu': 'ю', 'ya': 'я'
        };
    }

    getCyrillic(latinChar) {
        return this.translitMap[latinChar.toLowerCase()] || null;
    }

    getFriendshipStatus(cyrillicChar) {
        // Demo logic: True Friends (A, K, M, O, T), False (B, H, P, C, Y, X)
        const trueFriends = ['а', 'к', 'м', 'о', 'т'];
        const falseFriends = ['в', 'н', 'р', 'с', 'у', 'х'];
        if (trueFriends.includes(cyrillicChar)) return 'true';
        if (falseFriends.includes(cyrillicChar)) return 'false';
        return 'new';
    }

    // Check gender, heuristic...
}
