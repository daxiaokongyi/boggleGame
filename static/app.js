class BoggleGame {
    constructor(secs = 60){
        this.words = new Set();
        this.secs = secs;
        this.timer = setInterval(this.tick.bind(this), 1000);
        this.showTimer();
        $('.add_word').on('submit', this.handleSubmit.bind(this));
        // $('.choose_size').on('submit', this.handleSize.bind(this));
    }

    showMessage(msg, cls) {
        $('.msg').text('');
        $('.msg').text(msg).removeClass().addClass(`msg ${cls}`);
    }

    showScore(size) {
        $('.score').text(`${size}`); 
    }

    showWord(word){
        $('.words').append(`<li>${word}</li>`);
    }

    showTimer() {
        $('.timer').text(`Time Left: ${this.secs}`);
    }

    async tick() {
        this.secs -= 1;
        this.showTimer();
        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.gameResult();
        }
    }

    // async handleSize(evt) {
    //     evt.preventDefault();
    //     console.log($('.size').val());
    //     const res = await axios.post('/size', {size: $('.size').val()});
    // }

    async handleSubmit(evt) {
        evt.preventDefault();
        // Get input word from form
        let currentWord = $('.word').val();
        // if current word is empty, return
        if (!currentWord) return;
        // if current word already exists, shows exists message and return
        if (this.words.has(currentWord)) {
            this.showMessage(`${currentWord} already exists in the words`, 'err');
            return;
        }
        // get response from the server
        const res = await axios.get('/check_valid', {params: {word : currentWord}});
        
        if (res.data.result === 'ok') {
            this.showMessage(`${currentWord} is valid and added`, 'ok' );
            this.words.add(currentWord);
            this.showWord(currentWord);
        } else if (res.data.result === 'not-on-board') {
            this.showMessage(`${currentWord} is not a valid word in this board`, 'err');
        } else if (res.data.result === 'not-word') {
            this.showMessage(`${currentWord} is not a valid word`, 'err');
        }
        // reset word input
        $('.word').val('');
        // show the current score
        this.showScore(this.words.size);
    }   

    async gameResult() {
        // hide input
        $('.add_word').hide();
        const res = await axios.post('/post-score', {score: this.words.size});
        let highestScore = res.data['result'];
        let round = res.data['round'];

        if (this.words.size === highestScore && round > 1) {
            // $('.highest').text(`Congratulations! You got new record ${highestScore}`)
            this.showMessage(`Congratulations! You got new record ${highestScore}`, 'ok')
        } else {
            // $('.highest').text(`Your Highest Score is ${highestScore}`)
            this.showMessage(`Your Highest Score is ${highestScore}`, 'ok')
        }
        $('.round').text(`Your Round # ${round}`)
    }
}

