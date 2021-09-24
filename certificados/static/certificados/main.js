function att_formFiltro(operacao) {
    document.getElementById("id_operacao").value = operacao
}

function att_formValidarCertificado(operacao) {
    document.getElementById("id_operacao").value = operacao
}

function fechar_modal_menssagem() {
    document.getElementById("modal_menssagem").style.display = "none";
}

function dropdown() {
    document.getElementById("dropdown-content").style.display = "block";
}

function deletar_certificado() {
    var result = confirm("Esta é uma ação irreversível, deseja mesmo deletar o certificado?")
    if(result == true) {
        att_formValidarCertificado('deletar')
        document.getElementById('form-certificado').submit();
    }
}