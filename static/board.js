
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
            console.log('array = ', arr)
            console.log('$form = ', $form)
            console.log('opt = ', opt)
            console.log(' textContent => ', $('#textContent').code() )
            for(var i = 0; i < arr.length; i++) {

                if( arr[i].name === 'board_content') {
                    arr[i].value = $('#textContent').code()
                }

            }

            return true;
        },

        dataType: 'json',

        success: function(r, e,e1,e2) {
            consloe.log(r)
        },


    })
})