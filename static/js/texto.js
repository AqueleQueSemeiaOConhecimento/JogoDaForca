/* ENGENHARIA DA COMPUTAÇÃO */
$(document).ready(function() {
    let texto = 'E N G E N H A R I A - D A - C O M P U T A Ç Ã O';
    let index = 0;
    let velocidade = 75;

    $('#engenharia').text('');
    function digitar_engenharia_da_computacao() {
        if(index < texto.length) {
            $('#engenharia').append(texto.charAt(index));
            index++;
            setTimeout(digitar_engenharia_da_computacao, velocidade);
        }
    }

    digitar_engenharia_da_computacao()
})

