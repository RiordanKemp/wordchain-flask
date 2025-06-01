let timer = null;

function normalMode(normalbutton){
    let hardbutton = document.getElementById("hardButton"); 

    document.getElementById("diffreader").innerHTML = "Difficulty: <font color=green><b>NORMAL</b></font>";

    difficultyChosen(false)

    difficulty = "Disabled";

        $.ajax({
        url: '/setdifficulty',
        type: 'POST',
        data: { 'hardmode': difficulty },
        success: function(response) {
            //document.getElementById('output-diff').innerHTML = response;
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function hardMode(hardbutton, difficulty){
    let normalbutton = document.getElementById("normalButton");

    document.getElementById("diffreader").innerHTML = "Difficulty: <font color=red><b>HARD</b></font>";

    difficultyChosen(true)

    difficulty = "Enabled";  
    
    $.ajax({
        url: '/setdifficulty',
        type: 'POST',
        data: { 'hardmode': difficulty },
        success: function(response) {
            //document.getElementById('output-diff').innerHTML = response;
        },
        error: function(error) {
            console.log(error);
        }
    });

}

function difficultyChosen(diffBool){
    if (diffBool){
        document.getElementById("diffexpl").innerHTML = "You chose to play on Hard Mode. You will have up to 10 minutes to list as many words as possible, built from the letters of a random parent word."
    }
    else if (!diffBool){
        document.getElementById("diffexpl").innerHTML = "You chose to play on Normal Mode. You will have up to 10 minutes to list as many words as possible, built from the letters of a random parent word."
    }

    let mainbutton = document.getElementById("buttonmain");
    mainbutton.style.display = "flex";

    hidediffs = document.getElementsByClassName("hidediff");
    for (let element of hidediffs){
        element.style.display = "none";
    }

}

function runMain(){
    wordsubmits = document.getElementsByClassName("wordsubmission");
    for (let word of wordsubmits){
        word.style.display = "flex";
    }

    document.getElementById("buttonmain").style.display = "none";
    document.getElementById("diffexpl").style.display = "none";
    document.getElementById("fwtext").style.display = "block";
    document.getElementById("buttonreset").style.display = "block";

    $.ajax({
        url: '/main',
        type: 'POST',
        success: function(response) {
            var splityield = response.split('|')
            document.getElementById('outputparent').innerHTML = "Parent Word: " + splityield[0];
            document.getElementById('outputdef').innerHTML = splityield[1];
            starttimer();
    },
    error: function(error) {
        console.log(error);
    }
});


}

function starttimer(){
    let timetext = document.getElementById("timetext");

    timetext.innerHTML = "Starting soon...";
let timeLeft = 600; 

  timer = setInterval(() => {
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  string = "Time Left: " + (`${minutes}:${seconds < 10 ? '0' : ''}${seconds}`);
  document.getElementById("timetext").innerHTML = string;

  timeLeft--;

  if (timeLeft < 0) {
    clearInterval(timer);
      document.getElementById("timetext").innerHTML = ("Time Left: None");
      resetGame()
  }
}, 1000);
}


function submitFirstWord(){
   
    var userinput = document.getElementById('wordinput').value;
    document.getElementById('wordinput').value = "";

    $.ajax({
        url: '/first_word',
        type: 'POST',
        data: { 'input_str': userinput },
        success: function(response) {
            var splityield = response.split('|')
            var errormsg = splityield[0]
            var error = splityield[1]
            var wordchain = splityield[2]

            if (error == "NOERROR"){
            resetchildword(errormsg, wordchain);
            }
            else{
            document.getElementById('fail').innerHTML = errormsg;
            }


        },
        error: function(error) {
            console.log(error);
        }
    });
        
}

function resetchildword(prevword, wordchain){
    document.getElementById('fail').innerHTML = "";
    let buildletter = prevword.slice(-1).toUpperCase();
    document.getElementById('fwtext').innerHTML = "Enter a child word built from letters of the parent word, and <u>starting with the letter \"" + buildletter + "\"</u>.<br>If you are playing in Hard Mode, child words must be within +-2 length of the parent.";

    wordchaintext = document.getElementById('wordchain');
    wordchaintext.innerHTML = "My Chain: " + wordchain;

}

function submitChildWord(){
    var userinput = document.getElementById('childwordinput').value;
    document.getElementById('childwordinput').value = "";

    $.ajax({
        url: '/child_word',
        type: 'POST',
        data: { 'input_str': userinput },
        success: function(response) {
            var splityield = response.split('|')
            var errormsg = splityield[0]
            var error = splityield[1]
            var wordchain = splityield[2]

            if (error == "NOERROR"){
            resetchildword(errormsg, wordchain);
            }
            else{
            document.getElementById('fail').innerHTML = errormsg;
            }


        },
        error: function(error) {
            console.log(error);
        }
    });
}

function resetGame(){
    hidediffs = document.getElementsByClassName("rstremove");
    var chain;
    for (let element of hidediffs){
        element.style.display = "none";
    }

    document.getElementById("timetext").innerHTML = ("Time Left: None");
    clearInterval(timer)

}

const link = encodeURI(window.location.href);
const msg = encodeURIComponent("Hey, look at what I got at today's word chain!");
const title = encodeURIComponent(document.querySelector('title').textContent);

const fb = document.querySelector('.facebook');
fb.href = `https://www.facebook.com/share.php?u${link}`;