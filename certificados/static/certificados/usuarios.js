document.getElementById("barra_pesquisa").addEventListener("input", atualizar_certificados);

function atualizar_certificados() {
    $(".elementos_tabela").each(function(i, obj) {
        var x = document.getElementById("barra_pesquisa");
        var nome = document.getElementById(`nome_${obj.id}`);
        if (!eval(`(nome.innerHTML.match(/^${x.value}.*$/))`)) {
            document.getElementById(obj.id).style.display = "none";
        } else if (eval(`nome.innerHTML.match(/^${x.value}.*$/)`)) {
            document.getElementById(obj.id).style.display = "table-row";
        } 

        if (x.value == "") {
            document.getElementById(obj.id).style.display = "table-row";
        }
    });
}