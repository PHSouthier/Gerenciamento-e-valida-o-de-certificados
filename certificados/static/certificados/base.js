function nome_user_encurtado() {
    var nome = document.getElementById("nome_usuario").innerHTML;
    var sobrenome = document.getElementById("sobrenome_usuario").innerHTML;
    var div = document.getElementById("nome_user");
    var stringEncurtada = "";
    if ((nome.length + sobrenome.length) > 40) {
        var string = `${nome} ${sobrenome}`
        arrayString = string.split("");
        for(var i = 0; i < 40; i++) {
            stringEncurtada = stringEncurtada + arrayString[i]; 
        }
        div.innerHTML = `${stringEncurtada}...`;
    } else {
        div.innerHTML = `${nome} ${sobrenome}`;
    }
}