
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


//------------------
// 글쓰기 게시판으로 이동
var moveWriteForm = function(boardName) {
    window.location.href = '/board/' + boardName + '/write'
}

$(document).ready( function() {


    $('#boardForm').ajaxForm({
        beforeSubmit: function(arr, $form, opt) {
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
                history.back();
            }
            else {
                alert(r.data)
            }
        },


    })
})