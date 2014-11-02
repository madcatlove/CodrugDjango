
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