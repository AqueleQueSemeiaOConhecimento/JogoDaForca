/* PLAY */
$(document).ready(function() {
    $('#play').on('click', function() {
        console.log('clicou ze');
        $.ajax({
            url: '/jogo' ,
            method: 'GET',
            success: function(data) {
                $('.container-container').html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Erro na requisição AJAX:', textStatus, errorThrown);
            }
        });
    });


    $('#adivinharForm').submit(function(event) {
        event.preventDefault();
        const letra = $('#letra').val();
        $.ajax({
            url: '/adivinhar',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ letra: letra }),
            success: function(data) {
                updateGameState(data);
                updateImage(data);
                $('#letra').val('');
            },
            error: function(err) {
                console.log('Erro na requisição AJAX:', err);
            }
        });
    });

    function updateImage(data) {
        let vida = data.vidas;
        let caminho = ''
        switch (vida) {
            case 6:
                caminho = '/static/img/1.png';
                break;
            case 5:
                caminho = '/static/img/2.png';
                break;
            case 4:
                caminho = '/static/img/3.png';
                break;
            case 3:
                caminho = '/static/img/4.png';
                break;
            case 2:
                caminho = '/static/img/5.png';
                break;
            case 1:
                caminho = '/static/img/6.png';
                break;
            case 0:
                caminho = '/static/img/monkey.gif';
                break;
        }
        $('.personagem').attr('src', caminho);
    }

    function updateGameState(data) {
        $('.word').text(data.palavra);
        $('.vidas').text('Vidas restantes: ' + data.vidas);
        $('.letras_adivinhadas').text('Letras adivinhadas: ' + data.letras_adivinhadas.join(', '));
        $('.mensagem').text(data.mensagem);
    }
});
