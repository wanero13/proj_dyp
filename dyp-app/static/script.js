var entropy;
var passwordElem;
var password;
console.log('CCC');
document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        initApplication();
    }
}

function initApplication(){
    entropy = document.getElementById('entropy');
    passwordElem = document.forms[0]["password"];
    passwordElem.addEventListener('keyup', () => checkPass());
    console.log('BBB');
}

function checkPass() {
    password = passwordElem.value;
    var pool = 86;
    var length = password.length;
    var pe = Math.log2(Math.pow(pool, length));
    var inside = 'Strength: ' + pe.toString();
    entropy.innerHTML = inside;
    console.log('AAA');
}

