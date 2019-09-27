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

$(document).ready(function() {
    $("div.vote-block").each(function() {
        var objId = "div#" + $(this).attr('id');
        var vote_url = $(this).attr('dj-vote-url');
        console.log(objId, vote_url, $(this).attr('dj-init-data'));
        $(objId + ' button.vote-up').click(vote_handler(vote_url, objId, 'POST', 'up'));
        $(objId + ' button.vote-down').click(vote_handler(vote_url, objId, 'POST', 'down'));
        vote_updater(objId)($(this).attr('dj-init-data'));
    });
});

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

$(document).ready(function() {
    $("button.mark-answer").each(function() {
        var objId = "button#" + $(this).attr('id');
        var mark_url = $(this).attr('dj-mark-url');
        $(objId).click(mark_answer(mark_url, objId));
    });
});
