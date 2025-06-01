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
    document.getElementById("chaintop").style.display = "block";

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

  const fiveMinutes = 5 * 60 * 1000; // 5m in milliseconds
  const endTime = Date.now() + fiveMinutes;

  timer = setInterval(() => {
      const now = Date.now();
  const remaining = endTime - now;
//   const minutes = Math.floor(timeLeft / 60);
//   const seconds = timeLeft % 60;

 if (remaining <= 0) {
    clearInterval(timer);
    console.log("Countdown finished!");
  } else {
    const minutes = Math.floor(remaining / 1000 / 60);
    const seconds = Math.floor((remaining / 1000) % 60);

  string = "Time Left: " + (`${minutes}:${seconds < 10 ? '0' : ''}${seconds}`);
  document.getElementById("timetext").innerHTML = string;
 }
}, 1000)};


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
            var childmin = splityield[3]
            var childmax = splityield[4]

            if (error == "NOERROR"){
                resetchildword(wordchain);
                initial_word_done(childmin, childmax, errormsg);
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

function initial_word_done(childMin, childMax, prevword){
    document.getElementById('submitword').style.display = "none";
    document.getElementById('wordinput').style.display = "none";
    document.getElementById('submitchildword').style.display = "inline-block";
    document.getElementById('childwordinput').style.display = "inline-block";

    checkDifficulty(prevword, childMin, childMax);
}

function difficulty_update(difficulty, prevword, childmin, childmax){

    let buildletter = prevword.slice(-1).toUpperCase();

    if (difficulty == "F"){
    document.getElementById('fwtext').innerHTML = "Enter a child word built from letters of the parent word, and <u>starting with the letter \"" + buildletter + "\"</u>."
    }
    else{
        document.getElementById('fwtext').innerHTML = "Enter a child word built from letters of the parent word, and <u>starting with the letter \"" + buildletter + "\"</u>.<br>Since you are playing on Hard Mode, child words must be " + childmin + " to " + childmax + " letters.";
    }

}

function resetchildword(wordchain){
    document.getElementById('fail').innerHTML = "";

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
            var childmin = splityield[3]
            var childmax = splityield[4]

            if (error == "NOERROR"){
            resetchildword(wordchain);
            checkDifficulty(errormsg, childmin, childmax);

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
    clearInterval(timer);

    $.ajax({
    url: '/checkchain',
    type: 'POST',
    success: function(response) {
        chain_str = response;
        chainText = document.getElementById("wordchain");
        chainText.style.fontSize = "2em";
        chainText.innerHTML = chain_str;


    },
    error: function(error) {
        console.log(error);
    }
});


}

function checkDifficulty(prevword, childmin, childmax){
    $.ajax({
        url: '/checkdiff',
        type: 'POST',
        success: function(response) {
            difficulty = response;
            difficulty_update(difficulty, prevword, childmin, childmax);



        },
        error: function(error) {
            console.log(error);
        }
    });

}