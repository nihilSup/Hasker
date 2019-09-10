function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function vote_updater(id) {
    return function(response) {
        response = JSON.parse(response);
        if (response['user_ups'] != 0) {
            $(id + ' ' + 'button.vote-up').attr('disabled', true)
            $(id + ' ' + 'button.vote-down').attr('disabled', false)
        } else if (response['user_downs'] != 0) {
            $(id + ' ' + 'button.vote-down').attr('disabled', true)
            $(id + ' ' + 'button.vote-up').attr('disabled', false)
        } else if (response['user_ups'] == 0 && response['user_downs'] == 0) {
            $(id + ' ' + 'button.vote-down').attr('disabled', false)
            $(id + ' ' + 'button.vote-up').attr('disabled', false)
        }
        $(id + ' div.votes-count').html(response['votes']);
    }
}

function vote_handler(vote_url, id, reqType, voteType) {
    return function () {
        $.ajax({
            url: vote_url,
            type: reqType,
            data: reqType != 'POST'? {} : {
                vote_type: voteType,
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            dataType: 'html',
            success: vote_updater(id)
        });
    }
}

function mark_answer(_url, id) {
    return function () {
        $.ajax({
            url: _url,
            type: "POST",
            data: {
                is_correct: true,
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            dataType: 'html',
            success: function() {
                // this reload is needed to remove mark widgets if some answer was choisen
                location.reload();
            }
        });        
    }
}