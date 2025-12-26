let maxAttempts = 9;
let attempts = maxAttempts;
let answerNumbers = [];

const number1 = document.getElementById('number1');
const number2 = document.getElementById('number2');
const number3 = document.getElementById('number3');
const attemptsDisplay = document.getElementById('attempts');
const resultsContainer = document.getElementById('results');
const gameResultImg = document.getElementById('game-result-img');
const submitButton = document.querySelector('.submit-button');

initializeGame();

function initializeGame() {
    attempts = maxAttempts;
    answerNumbers = [];
    
    attemptsDisplay.innerText = attempts;
    resultsContainer.innerHTML = '';
    number1.value = '';
    number2.value = '';
    number3.value = '';
    gameResultImg.src = ''; 
    submitButton.disabled = false;
    
    while (answerNumbers.length < 3) {
        const randomNum = Math.floor(Math.random() * 10);
        if (!answerNumbers.includes(randomNum)) {
            answerNumbers.push(randomNum);
        }
    }
    console.log("정답(테스트용):", answerNumbers);
}

function check_numbers() {
    const val1 = number1.value;
    const val2 = number2.value;
    const val3 = number3.value;
    const userInputs = [val1, val2, val3];

    if (val1 === '' || val2 === '' || val3 === '') {
        clearInputs();
        return;
    }

    const inputNumbers = userInputs.map(num => parseInt(num));
    
    let strike = 0;
    let ball = 0;

    for (let i = 0; i < 3; i++) {
        if (inputNumbers[i] === answerNumbers[i]) {
            strike++;
        } else if (answerNumbers.includes(inputNumbers[i])) {
            ball++;
        }
    }

    const resultDiv = document.createElement('div');
    resultDiv.style.cssText = `
        display: flex; 
        align-items: center; 
        justify-content: center; 
        width: 100%; 
        margin-bottom: 15px; 
        font-size: 1.3rem; 
        font-family: 'Jua', sans-serif;
        border-bottom: 1px solid #eee; 
        padding-bottom: 5px;
    `;

    const numBoxStyle = "flex: 1; text-align: right; padding-right: 40px; font-weight: bold; letter-spacing: 5px;";
    const colonStyle = "flex: 0 0 auto; font-weight: bold; color: #555;"; 
    const scoreBoxStyle = "flex: 1; display: flex; align-items: center; justify-content: flex-start; padding-left: 40px; gap: 10px;";
    
    const circleBase = "display: inline-flex; justify-content: center; align-items: center; width: 28px; height: 32px; border-radius: 50%; font-weight: bold; font-size: 1.1rem;";
    const strikeStyle = `background-color: #009900; color: white; ${circleBase}`;
    const ballStyle = `background-color: #FFFF00; color: black; ${circleBase}`;

    let resultHTML = '';

    const inputDisplay = `<div style="${numBoxStyle}">${val1} ${val2} ${val3}</div>`;
    const colonDisplay = `<div style="${colonStyle}">:</div>`;

    if (strike === 0 && ball === 0) {
        resultHTML = `
            ${inputDisplay}
            ${colonDisplay}
            <div style="${scoreBoxStyle}">
                <span style="color: red; font-weight: bold;">O</span>
            </div>
        `;
    } else {
        resultHTML = `
            ${inputDisplay}
            ${colonDisplay}
            <div style="${scoreBoxStyle}">
                <span>${strike}</span><div style="${strikeStyle}">S</div>
                <span>${ball}</span><div style="${ballStyle}">B</div>
            </div>
        `;
    }

    resultDiv.innerHTML = resultHTML;
    resultsContainer.appendChild(resultDiv); 

    attempts--;
    attemptsDisplay.innerText = attempts;

    if (strike === 3) {
        endGame('win');
    } else if (attempts === 0) {
        endGame('lose');
    } else {
        clearInputs();
        number1.focus();
    }
}

function clearInputs() {
    number1.value = '';
    number2.value = '';
    number3.value = '';
}

function endGame(result) {
    submitButton.disabled = true;
    if (result === 'win') {
        gameResultImg.src = 'success.png';
    } else if (result === 'lose') {
        gameResultImg.src = 'fail.png';
    }
}