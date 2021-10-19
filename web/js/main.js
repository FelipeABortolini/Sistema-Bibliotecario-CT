function login() {
    var senha = document.getElementById("senha").value;
    eel.login(senha);
}

eel.expose(mensagem)
function mensagem(texto) {
    alert(texto);
}

eel.expose(redireciona_index)
function redireciona_index() {
    window.location.replace("index.html");
}

function altera_tela_atual(nome_tela) {
    eel.altera_tela_atual(nome_tela);
}

function go(tela){
    window.location.replace(tela);
}

function goEditarLivro(){
    var array = [];
    var livros = document.getElementById("editar");
    var checkboxes = livros.querySelectorAll('input[type=checkbox]:checked');
    if(checkboxes.length == 1){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
        eel.regitra_editavel_bd(array);
        go('editar1.html');
    } else if(checkboxes.length > 1){
        alert('Selecione apenas um livro para editar!');
    } else {
        alert('Selecione um livro para editar!');
    }
}

function editarLivro(){
    eel.busca_editavel()(procura_edicoes);
}

function procura_edicoes(lista){
    var nome_atual = lista[0][0];
    var autor_atual = lista[0][1];
    var exemplares_atual = lista[0][2];
    var disponiveis_atual = lista[0][5];
    var id = lista[0][4];

    var alugados = exemplares_atual - disponiveis_atual;

    var nome_editado = document.getElementById('nomeEditar').value;
    var autor_editado = document.getElementById('autorEditar').value;
    var exemplares_editado = document.getElementById('exemplaresEditar').value;

    if(nome_editado!=""){
        nome_atual = nome_editado;
    }
    if(autor_editado!=""){
        autor_atual = autor_editado;
    }
    if(exemplares_editado!=""){
        exemplares_atual = exemplares_editado;
        disponiveis_atual = exemplares_atual - alugados;
        if(disponiveis_atual < 0){
            disponiveis_atual = 0;
            exemplares_atual = alugados;
        }
    }

    eel.editar_livro(nome_atual, autor_atual, exemplares_atual, disponiveis_atual, id);
}

function informacoes_livro_placeholder(){
    eel.busca_editavel()(insere_placeholder);
}

function insere_placeholder(lista){
    document.getElementById("nomeEditar").placeholder = lista[0][0];
    document.getElementById("autorEditar").placeholder = lista[0][1];
    document.getElementById("exemplaresEditar").placeholder = lista[0][2];
}

function altera_tela_atual(nome_tela) {
    eel.altera_tela_atual(nome_tela);
}

function titleize(sentence) {
    if(!sentence.split) return sentence;
    var _titleizeWord = function(string) {
            return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
        },
        result = [];
    sentence.split(" ").forEach(function(w) {
        result.push(_titleizeWord(w));
    });
    return result.join(" ");
}

function testeCadastraLivro(){
    var nome = titleize(document.getElementById("nome").value);
    var autor = titleize(document.getElementById("autor").value);
    var exemplares = document.getElementById("exemplares").value;

    if(nome && autor && exemplares){
        eel.testaLivro(nome, autor)(cadastraLivro);
    } else {
        alert("Preencha todos os campos!");
    }
}

function alteraSenha(){
    var senhaAtual = document.getElementById('idSenhaAtual').value;
    var novaSenha = document.getElementById('idNovaSenha').value;
    var confirma = document.getElementById('confirma').value;

    if(novaSenha != confirma){
        alert('A senha de confirmação não correponde à nova senha, tente novamente!');
    } else {
        eel.alteraSenha(senhaAtual, novaSenha);
        go('suporte.html');
    }
}

function cadastraLivro(cond){
    if(!cond) return false;

    var nome = titleize(document.getElementById("nome").value);
    var autor = titleize(document.getElementById("autor").value);
    var exemplares = document.getElementById("exemplares").value;

    if(nome && autor && exemplares){
        eel.insereLivroBD(nome, autor, exemplares);
        go('cadastrar.html')
    } else {
        alert("Preencha todos os campos!");
    }
}

eel.expose(sucCadastroHistorico)
function sucCadastroHistorico(){
    removeAluguelBD();
    alert('Registro de devolução efetuado com sucesso!');
    go('devolucao.html');
}

eel.expose(sucRenovacao)
function sucRenovacao(){
    alert('Renovação efetuada com sucesso!');
    go('devolucao.html');
}

function busca_checkbox2(){
    var select = document.getElementById('selectEmAberto').value;

    eel.busca('emAberto')(remove_checkbox);
    eel.busca_select_aberto(select)(insere_checkbox);
}

function busca_checkbox1(){
    var select = document.getElementById('selectHistorico').value;

    eel.busca('historico')(remove_checkbox);
    eel.busca_select(select)(insere_checkbox);
}

function busca_checkbox(tipo) {
    if(tipo == 'emAberto' || tipo == 'historico') eel.busca(tipo)(remove_checkbox);
    eel.busca(tipo)(insere_checkbox);
}

function buscaEmAberto(){
    var info = document.getElementById("buscaAberto").value;
    if(info != ''){
        eel.busca('emAberto')(remove_checkbox);
        eel.buscaPesquisa(info, 'emAberto')(insere_checkbox);
    } else {
        busca_checkbox('emAberto');
    }
}

function buscaHistoric(){
    var info = document.getElementById("buscaHistorico").value;
    if(info != ''){
        eel.busca('historico')(remove_checkbox);
        eel.buscaPesquisa(info, 'historico')(insere_checkbox);
    } else {
        busca_checkbox('historico');
    }
}

function buscaDateHistoric(){
    var offset = new Date().getTimezoneOffset();
    var info = new Date(document.getElementById("buscaDataHistorico").value);
    info.setMinutes(info.getMinutes() + offset);
    info = info.toISOString().slice(0, 19).replace('T', ' ');

    var checks = document.getElementById("checksHistorico");
    var checkboxes = checks.querySelectorAll('input[type=checkbox]:checked');
    if(checkboxes.length == 0) {
        alert('Selecione uma opção para buscar por data!');
        return false;
    } else if(checkboxes.length > 1) {
        alert('Selecione apenas uma opção para buscar por data!');
        return false;
    }

    var marcado;

    if(checkboxes[0].id == 'checkRetirada') marcado = 'retirada';
    else if(checkboxes[0].id == 'checkPrazo') marcado = 'prazo';
    else if(checkboxes[0].id == 'checkEntrega') marcado = 'entrega';

    eel.busca('historico')(remove_checkbox);
    eel.buscaDateHist(marcado, info)(insere_checkbox);
}

function buscaAtual(){
    eel.getParam()(insereAtual);
}

function insereAtual(lista){
    var inputPeriodo = document.getElementById('periodoAtual');
    var inputValor = document.getElementById('valorAtual');

    var valor = lista[1];
    var periodo = lista[0];

    if(typeof(valor) == 'string'){
        valor = parseFloat(valor);
    }

    valor = valor.toFixed(2);
    valor = valor.toString().replace('.', ',');

    if(periodo == 1) inputPeriodo.value = String(periodo+' dia');
    else inputPeriodo.value = String(periodo+' dias');
    inputPeriodo.setAttribute('style', 'color: white; background-color: gray; width: 10%; height: 15%; border-radius: 10px; padding-left: 5px');
    inputValor.value = String('R$ '+valor);
    inputValor.setAttribute('style', 'color: white; background-color: gray; width: 10%; height: 15%; border-radius: 10px; padding-left: 5px');
}

function atualizaParam(){
    var periodo = document.getElementById('periodo').value;
    var valor = document.getElementById('valor').value;

    if(periodo == '' && valor == ''){
        alert('Preencha pelo menos um dos campos para atualizar os parâmetros!');
        return false;
    }

    if (periodo != '' && periodo <= 0){
        alert('O período não pode ser menor ou igual a 0!');
        return false;
    } else if (valor < 0){
        alert('O valor não pode ser menor que 0!');
        return false;
    }

    if(periodo == '') eel.atualizaParamVal(valor);
    else if(valor == '') eel.atualizaParamPer(periodo);
    else eel.atualizaParam(periodo, valor);

    alert('Parâmetros atualizados com sucesso!');
    go('devolucao.html');
}

function buscaRemover(){
    eel.busca_num('remover')(remove_checkbox);

    var info = document.getElementById("buscaRem").value;
    eel.buscaPesquisa(info, 'remover')(insere_checkbox);
}

function buscaListar(){
    eel.busca('listar')(remove_checkbox);

    var info = document.getElementById("buscaList").value;
    eel.buscaPesquisa(info, 'listar')(insere_checkbox);
}

function buscaRetirada(){
    eel.busca_num('retirada')(remove_checkbox);

    var info = document.getElementById("buscaRet").value;
    eel.buscaPesquisa(info, 'retirada')(insere_checkbox);
}

function buscaDevolucao(){
    eel.busca('devolucao')(remove_checkbox);

    var info = document.getElementById("buscaDev").value;
    eel.buscaAluno(info, 'devolucao')(insere_checkbox);
}

function buscaEditar(){
    eel.busca('editar')(remove_checkbox);

    var info = document.getElementById("buscaEdi").value;
    eel.buscaPesquisa(info, 'editar')(insere_checkbox);
}

function insere_checkbox(lista) {
    var id = lista.pop();
    var select = document.getElementById(id);
    var opcao;

    if(id != 'retirada' && id != 'remover'){
        for (var i = 0; i < lista.length; i+=2) {
            if(id=='emAberto' || id=='historico' || id=='listar'){
                opcao = document.createElement("li");
                opcao.setAttribute('style', 'float: left; position: relative; top: 3.5%; margin-left: -95%;');
            }else{
                opcao = document.createElement("input");
                opcao.type = "checkbox";
                opcao.setAttribute('style', 'float: left; position: relative; top: 5px;');
            }
            opcao.id = lista[i];
            opcao.className = 'opt';
            opcao.value = lista[i];

            var label = document.createElement("label");
            label.appendChild(document.createTextNode(lista[i+1]));
            label.setAttribute('style', 'float: left; letter-spacing: 2px; position: relative; top: -7.75%; left: 2.5%; text-align: left; font-size: 15px;');
            label.id = "labelopt";

            var br = document.createElement("br");
            br.id = "br";

            select.appendChild(opcao);
            select.appendChild(label);
            select.appendChild(br);
        }
    } else if(id == 'retirada'){
        for (var i = 0; i < lista.length; i+=3) {
            var opcao = document.createElement("input");
            opcao.type = "checkbox";
            opcao.id = lista[i];
            opcao.className = 'opt';
            opcao.value = lista[i];
            opcao.setAttribute('style', 'float: left; position: relative; top: 5px');

            var label = document.createElement("label");
            label.appendChild(document.createTextNode(lista[i+2]));
            label.setAttribute('style', 'float: left; letter-spacing: 1px; position: relative; top: -8.5%; left: 4.5%; text-align: left; font-size: 75%;');
            label.id = lista[i+1];

            var br = document.createElement("br");
            br.id = "br";

            select.appendChild(opcao);
            select.appendChild(label);
            select.appendChild(br);
        }

        eel.busca('retirada1')(enable_opts_ret);
    } else {
        for (var i = 0; i < lista.length; i+=3) {
            var opcao = document.createElement("input");
            opcao.type = "checkbox";
            opcao.id = lista[i];
            opcao.className = 'opt';
            opcao.value = lista[i];
            opcao.setAttribute('style', 'float: left; position: relative; top: 5px');

            var label = document.createElement("label");
            label.appendChild(document.createTextNode(lista[i+2]));
            //label.setAttribute('style', 'float: left; letter-spacing: 2px; margin-left: 5px; text-align: left');
            label.setAttribute('style', 'float: left; letter-spacing: 2px; position: relative; top: -8%; left: 2.5%; text-align: left; font-size: 15px;');
            label.id = lista[i+1];

            var br = document.createElement("br");
            br.id = "br";

            select.appendChild(opcao);
            select.appendChild(label);
            select.appendChild(br);
        }

        eel.busca('remover1')(enable_opts_rem);
    }
}

function enable_opts_ret(lista){
    var select = document.getElementById('retirada');

    var options = select.querySelectorAll('input[type=checkbox]');
    var label;

    for (var i = 0; i < options.length; i++) {
        for (var j = 0; j < lista.length; j+=3) {
            if (options[i].value == lista[j]) {
                if(lista[j+2] == 0){
                    options[i].disabled = true;
                    options[i].setAttribute('style', 'float: left; position: relative; top: 5px');
                    label = document.querySelectorAll('label');
                    for(var k = 0; k < label.length; k++){
                        if(label[k].id==i){
                            label[k].setAttribute('style', 'color: #c2c1c1; float: left; letter-spacing: 2px; margin-left: 5px; text-align: left');
                        }
                    }
                    break;
                }
            }
        }
    }
}

function enable_opts_rem(lista){
    var select = document.getElementById('remover');

    var options = select.querySelectorAll('input[type=checkbox]');
    var label;

    for (var i = 0; i < options.length; i++) {
        for (var j = 0; j < lista.length; j+=4) {
            if (options[i].value == lista[j]) {
                if(lista[j+2] != lista[j+3]){
                    options[i].disabled = true;
                    options[i].setAttribute('style', 'float: left; position: relative; top: 5px');
                    label = document.querySelectorAll('label');
                    for(var k = 0; k < label.length; k++){
                        if(label[k].id==i){
                            label[k].setAttribute('style', 'color: #c2c1c1; float: left; letter-spacing: 2px; margin-left: 5px; text-align: left');
                        }
                    }
                    break;
                }
            }
        }
    }
}

function remove_checkbox(lista){
    var id = lista.pop();
    var label;
    var num = lista[0];

    if(id=='retirada'){
        for(var i = 0; i < num; i+=1) {
            document.getElementsByClassName('opt')[0].remove();
            label = document.querySelectorAll('label');
            for(var k = 1; k < label.length; k+=2){
                if(label[k].id==i){
                    label[k].remove();
                    break;
                }
            }
            document.getElementById('br').remove();
        }
    } else if(id=='remover'){
        for(var i = 0; i < num; i+=1) {
            document.getElementsByClassName('opt')[0].remove();
            label = document.querySelectorAll('label');
            for(var k = 1; k < label.length; k+=2){
                if(label[k].id==i){
                    label[k].remove();
                    break;
                }
            }
            document.getElementById('br').remove();
        }
    } else {
        for (var i = 0; i < lista.length; i+=2) {
            document.getElementsByClassName('opt')[0].remove();
            document.getElementById('labelopt').remove();
            document.getElementById('br').remove();
        }
    }
}

function testaRemoverLivros(){
    var array = [];
    var livros = document.getElementById("remover");
    var checkboxes = livros.querySelectorAll('input[type=checkbox]:checked');
    if(checkboxes.length == 0){
        alert('Selecione pelo menos um livro para remover da lista!');
        return false;
    }
    for (var i = 0; i < checkboxes.length; i++) {
        array.push(checkboxes[i].value);
    }
    eel.removerLivros(array)(redirecionaRem);
}

function redirecionaRem(cond){
    if(cond) go('remover.html')
}

function testeAlunoRetirada(){
    var array = [];
    var livros = document.getElementById("retirada");
    var checkboxes = livros.querySelectorAll('input[type=checkbox]:checked');
    if(checkboxes.length <= 3 && checkboxes.length > 0){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
    } else if(checkboxes.length > 3){
        alert('Um aluno pode retirar no máximo 3 livros por vez!');
        return false;
    } else {
        alert('Selecione um livro para a retirada!');
        return false;
    }

    var nomeGuerra = titleize(document.getElementById("nomeGuerra").value);
    var turma = document.getElementById("turma").value;
    if(nomeGuerra == ''){
        alert('Insira o nome de guerra do aluno!');
        return false;
    } else if(turma == ''){
        alert('Insira a turma do aluno!');
        return false;
    }
    eel.registraAluno(nomeGuerra, turma);

    eel.testeAlugueisAluno(array, nomeGuerra)(registraRetirada);
}

function disableFirstOpt(){
    var opt = document.getElementById('firstOpt');
    opt.setAttribute('disabled', '');
}

function registraRetirada(cond){

    if(!cond) return false;

    var array = [];
    var livros = document.getElementById("retirada");
    var checkboxes = livros.querySelectorAll('input[type=checkbox]:checked');
    if(checkboxes.length <= 3 && checkboxes.length > 0){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
    } else if(checkboxes.length > 3){
        alert('Um aluno pode retirar no máximo 3 livros por vez!');
        return false;
    } else {
        alert('Selecione um livro para a retirada!');
        return false;
    }

    var nomeGuerra = titleize(document.getElementById("nomeGuerra").value);
    var turma = document.getElementById("turma").value;
    if(nomeGuerra == ''){
        alert('Insira o nome de guerra do aluno!');
        return false;
    } else if(turma == ''){
        alert('Insira a turma do aluno!');
        return false;
    }
    eel.registraAluno(nomeGuerra, turma);

    eel.testeAlugueisAluno(array, nomeGuerra);

    if(document.getElementById("inputDataRetirada").value == ''){
        alert('Insira a data de retirada!');
        return false;
    }

    var offset = new Date().getTimezoneOffset();
    var dataRetirada = new Date(document.getElementById("inputDataRetirada").value);
    var dataEntrega = new Date(document.getElementById("inputDataRetirada").value);
    dataRetirada.setMinutes(dataRetirada.getMinutes() + offset);
    dataEntrega.setMinutes(dataEntrega.getMinutes() + offset);

    if(document.getElementById("diasRetirada").value == ''){
        alert('Insira a quantidade de dias até a entrega!');
        return false;
    }

    var dias = parseInt(document.getElementById("diasRetirada").value);

    if(dias > 15){
        alert('O tempo máximo permitido para ficar com os livros é 15 dias!')
        return false;
    } else if(dias <= 0 || dias == ''){
        alert('Insira um tempo para ficar com os livros maior que 0 dias!')
        return false;
    }
    dataEntrega.setDate(dataEntrega.getDate() + dias);

    dataEntrega = dataEntrega.toISOString().slice(0, 19).replace('T', ' ');
    dataRetirada = dataRetirada.toISOString().slice(0, 19).replace('T', ' ');

    eel.atualizaDisponiveis(array);

    eel.registraRetirada(array, nomeGuerra, dataRetirada, dataEntrega)(atualizaRetirada);
}

function registroDevolucao(param){

    var array = [];
    var retiradas = document.getElementById("devolucao");
    var checkboxes = retiradas.querySelectorAll('input[type=checkbox]:checked');

    if(checkboxes.length == 1){

        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }

        if (param == 0){
            eel.buscaDataDevolução(array)(calculaMulta);
        } else if (param == 1){
            eel.buscaDataDevolução(array)(registraDevolucao);
        } else if (param == 2){
            eel.buscaDataDevolução(array)(registroRenovacao);
        }

    } else if(checkboxes.length > 1) {

        if(param == 1){
            alert('Selecione um registro por vez para a devolução!');
        } else if(param == 2){
            alert('Selecione um registro por vez para a renovação!');
        } else if(param == 0){
            alert('Selecione um registro por vez para a realizar o cálculo da multa!');
        }
        return false;

    } else {

        if(param == 1){
            alert('Selecione um registro para a devolução!');
        } else if(param == 2){
            alert('Selecione um registro para a renovação!');
        } else if(param == 0){
            alert('Selecione um registro para a realizar o cálculo da multa!');
        }
        return false;
    }
}

function registraDevolucao(lista){

    var prazoEntrega = lista[0];

    var array = [];
    var retiradas = document.getElementById("devolucao");
    var checkboxes = retiradas.querySelectorAll('input[type=checkbox]:checked');

    if(checkboxes.length == 1){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
    } else if(checkboxes.length > 1){
        alert('Selecione um regitro por vez para realizar a devolução!');
        return false;
    } else {
        alert('Selecione um registro para a devolução!');
        return false;
    }

    if(document.getElementById("inputDataDevolucao").value == ''){
        alert('Insira uma data de devolução!');
        return false;
    } else {

        var offset = new Date().getTimezoneOffset();
        var dataDevolucao = new Date(document.getElementById("inputDataDevolucao").value);
        dataDevolucao.setMinutes(dataDevolucao.getMinutes() + offset);
        dataDevolucao = dataDevolucao.toISOString().slice(0, 19).replace('T', ' ');
        dataDevolucao1 = dataDevolucao.slice(0, 10);

        const prazo = moment(prazoEntrega);
        const devolucao = moment(dataDevolucao1);

        var diasUteis = calcBusinessDays(prazo, devolucao);

        if(diasUteis < 0){
            diasUteis = 0;
        }

        var valorMulta = 0.5;
        var diasParaCobranca = 1;

        var multa = (valorMulta * (diasUteis / diasParaCobranca)).toFixed(2);

        eel.atualizaDisponiveisUp(array);

        eel.registraHistorico(array, dataDevolucao, multa);
    }
}

function registroRenovacao(){

    var array = [];
    var retiradas = document.getElementById("devolucao");
    var checkboxes = retiradas.querySelectorAll('input[type=checkbox]:checked');

    if(checkboxes.length == 1){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
    } else if(checkboxes.length > 1){
        alert('Selecione um regitro por vez para realizar a renovação!');
        return false;
    } else {
        alert('Selecione um registro para a renovação!');
        return false;
    }

    if(document.getElementById("diasRenovarDev").value == ''){
        alert('Insira a quantidade dias para a renovação!');
        return false;
    } else {
        eel.buscaDataDevolução(array)(renova_aluguel);
    }
}

function renova_aluguel(lista){

    var prazoEntrega = lista[0];
    const prazo = moment(prazoEntrega);

    var diasRenovar = document.getElementById('diasRenovarDev').value;

    prazo.add(diasRenovar, 'd')

    var datePrazo = new Date(prazo)
    var offset = new Date().getTimezoneOffset();
    datePrazo.setMinutes(datePrazo.getMinutes() + offset);
    datePrazo = datePrazo.toISOString().slice(0, 19).replace('T', ' ');

    var array = [];
    var retiradas = document.getElementById("devolucao");
    var checkboxes = retiradas.querySelectorAll('input[type=checkbox]:checked');

    if(checkboxes.length == 1){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
    } else if(checkboxes.length > 1){
        alert('Selecione um regitro por vez para realizar renovação!');
        return false;
    } else {
        alert('Selecione um registro para a renovação!');
        return false;
    }

    eel.renovaAluguel(array, datePrazo);
}

function removeAluguelBD(){
    var array = [];
    var retiradas = document.getElementById("devolucao");
    var checkboxes = retiradas.querySelectorAll('input[type=checkbox]:checked');

    if(checkboxes.length == 1 && document.getElementById("inputDataDevolucao").value != ''){
        for (var i = 0; i < checkboxes.length; i++) {
            array.push(checkboxes[i].value);
        }
        eel.removerAluguelBD(array);
    } else {
        return false;
    }
}

function calculaMulta(lista){

    var valorMulta = lista.pop()
    var diasParaCobranca = lista.pop()

    var prazoEntrega = lista[0];

    if(document.getElementById("inputDataDevolucao").value == ''){
        alert('Insira uma data de devolução para que se possa realizar o cálculo!');
        return false;
    }

    var offset = new Date().getTimezoneOffset();
    var dataDevolucao = new Date(document.getElementById("inputDataDevolucao").value);
    dataDevolucao.setMinutes(dataDevolucao.getMinutes() + offset);
    dataDevolucao = dataDevolucao.toISOString().slice(0, 19).replace('T', ' ');
    dataDevolucao = dataDevolucao.slice(0, 10);

    const prazo = moment(prazoEntrega);
    const devolucao = moment(dataDevolucao);

    var diasUteis = calcBusinessDays(prazo, devolucao);

    if(diasUteis < 0){
        diasUteis = 0;
    }

    if(diasUteis == 1) document.getElementById('inputDiasAtraso').value = String(diasUteis+' dia');
    else document.getElementById('inputDiasAtraso').value = String(diasUteis+' dias');

    var multa = (valorMulta * (diasUteis / diasParaCobranca)).toFixed(2);

    document.getElementById('inputMulta').value = String('R$ '+multa);
}

function calcBusinessDays(startDate, endDate) {
    var feriados = [moment('2021-01-01').format("DD/MM"), moment('2021-04-21').format("DD/MM"), moment('2021-05-01').format("DD/MM"), moment('2021-09-07').format("DD/MM"), moment('2021-10-12').format("DD/MM"), moment('2021-11-02').format("DD/MM"), moment('2021-11-15').format("DD/MM"), moment('2021-12-25').format("DD/MM")];
    var day = moment(startDate);
    var businessDays = 0;

    if(day.isSameOrBefore(endDate,'day')){
        while (day.isSameOrBefore(endDate,'day')) {
            if (day.day()!=0 && day.day()!=6) businessDays++;
            for(var i = 0; i < feriados.length; i++){
                if(day.format("DD/MM") == feriados[i]) businessDays--;
            }
            day.add(1,'d');
        }
        if(businessDays != 0) businessDays--;
    } else {
        while (day.isAfter(endDate,'day')) {
            if (day.day()!=0 && day.day()!=6) businessDays--;
            for(var i = 0; i < feriados.length; i++){
                if(day.format("DD/MM") == feriados[i]) businessDays++;
            }
            day.add(-1,'d');
        }
        if(businessDays != 0) businessDays++;
    }
    return businessDays;
}

function atualizaRetirada(condition){
    if(condition){
        go("retirada.html");
    }
}