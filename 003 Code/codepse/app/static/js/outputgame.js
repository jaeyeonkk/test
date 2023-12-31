let allQuestions  = [];
let questions = [];  // Will be populated when user chooses a language
let userLanguage;  // To store user's chosen language
let currentQuestionIndex = 0;
let score = 0;
let userAnswers = [];
let username;

function startQuiz() {
    username = document.getElementById("username").value;
    userLanguage = document.getElementById("languageSelect").value;  // Get user's language choice

    fetch('/api/get_outputgame_questions')
    .then(response => response.json())
    .then(data => {
      allQuestions = data;

     // 사용자가 "Random"을 선택한 경우 모든 언어의 질문을 포함, 아니라면 선택한 언어의 질문만 포함
  if(userLanguage === "random") {
    questions = allQuestions;
  } else {
    questions = allQuestions.filter(q => q.language === userLanguage);
  }
  questions = questions.sort(() => Math.random() - 0.5).slice(0, 5);

    document.getElementById("login-section").style.display = "none";
    document.getElementById("quiz-section").style.display = "block";
    loadQuestion();
});
}

function loadQuestion() {
    if (currentQuestionIndex < questions.length) {
        document.getElementById("question").innerHTML = '<pre>' + questions[currentQuestionIndex].question + '</pre>';
    } else {
        document.getElementById("quiz-section").style.display = "none";
        let resultText = "문제를 모두 풀었습니다! Your score is: " + score + "<br/><br/>";
        for (let i = 0; i < questions.length; i++) {
            resultText += `<span class="highlight">Question: <br/>${questions[i].question}<br/><br/>Your answer: ${userAnswers[i].answer}<br/><br/><span class="correct-answer">Correct answer: ${questions[i].answer}</span><br/><br/>`;

        }
        document.getElementById("result").innerHTML = resultText;

        let leaderboard = JSON.parse(localStorage.getItem(userLanguage + "Leaderboard") || "[]");
        leaderboard.push({ username: username, score: score });
        leaderboard.sort((a, b) => b.score - a.score);
        localStorage.setItem(userLanguage + "Leaderboard", JSON.stringify(leaderboard));
            
        let leaderboardText = " ハ____ハ ｡ﾟﾟ･｡･ﾟﾟ｡<br> ꒰ ⬩ ω ⬩ ꒱  ˚｡.............｡˚ <br>| つ ~ good　ﾟ ･｡･ﾟ</br><h2>Leaderboard for " + userLanguage + "★</h2><br/><br/>";
        for (let i = 0; i < leaderboard.length; i++) {
            leaderboardText += `${i + 1}. ${leaderboard[i].username}: ${leaderboard[i].score}<br/><br/>`;  
        }
        document.getElementById("leaderboard").innerHTML = leaderboardText;

    }
}

function submitAnswer() {
    let userAnswer = document.getElementById("answer").value;
    if (userAnswer.toLowerCase() === questions[currentQuestionIndex].answer.toLowerCase()) {
        score++;
    }
    userAnswers.push({ answer: userAnswer });
    document.getElementById("answer").value = "";
    currentQuestionIndex++;
    loadQuestion();
}