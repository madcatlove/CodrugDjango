
var _boardCls = (function() {
       var obj = {}

    obj.getData = function() {
        var $board = $('#boardContent input')

        var title = $board.eq(0).val().trim()
        var content = $('#textContent').code()

        return {
            title : title,
            content : content,
        }
    }

    obj.submitData = function() {
        console.log( this.getData() )
    }


    return obj;
})()

var procModifyArticle = function(id, boardNAME) {
    var $board_title = $('input[name=board_title]').val().trim();
    var $board_content = $('#textContent').code();

    if( $board_title.length == 0) {
        alert(' 제목을 입력해주세요. ');
        return;
    }

    if( $board_content.length == 0) {
        alert(' 내용을 입력해주세요. ');
        return;
    }

    var sParam = {
        board_title : $board_title,
        board_content : $board_content,
    }

    urlReq.post('/board/' + boardNAME + '/modify/' + id, sParam, function(result) {
        if( !result.error ) {
            alert(' 정상적으로 수정이 되었습니다. ');
            window.location.href = '/board/' + boardNAME + '/detail/' + id;
        }
        else {
            alert( result.data )
        }
    })

}


//------------------
// 글쓰기 게시판으로 이동
var moveWriteForm = function(boardName) {
    window.location.href = '/board/' + boardName + '/write'
}

$(document).ready( function() {


    $('#boardForm').ajaxForm({
        beforeSubmit: function(arr, $form, opt) {
            console.log(arr, $form, opt)

            for(var i = 0; i < arr.length; i++) {

                if( arr[i].name === 'board_content') {
                    arr[i].value = $('#textContent').code()
                }

            }

            return true;
        },

        dataType: 'json',

        success: function(r, e,e1,e2) {
            if ( typeof r === 'string') r = JSON.parse(r);

            if(r.error == false) {
                alert(' 정상적으로 글을 작성하였습니다. ')
                window.location.href = '/board/' + r.data;
            }
            else {
                alert(r.data)
            }
        },


    })
})

var closeQnAArticle = function(seq) {
    urlReq.get('/board/qna/close/' + seq, {}, function(result) {
        if( result.error == false) {
            alert(' 처리가 완료되었습니다. ');
            window.location.reload();
        }
        else {
            alert( result.data );
        }
    })
}

// --- 글수정 폼으로 ---
var moveModifyForm = function(id, boardNAME) {
    window.location.href = '/board/' + boardNAME + '/modify/' + id;
}

// --- 글삭제 ---
var moveDeleteForm = function(id, boardNAME) {
    if( confirm(' 게시물을 정말 삭제하시겠습니까? ') )
        window.location.href = '/board/' + boardNAME + '/delete/' + id;
}