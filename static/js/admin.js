
var modifyMemberInfo = function( $oJquery ) {
    var row = $oJquery.parent().siblings();

    var memberSeq = parseInt( row.eq(0).html() );
    var memberEmail = row.eq(1).html().trim();
    var memberName = row.eq(2).find('input').first().val().trim();
    var memberLevel = row.eq(3).find('input').first().val().trim();
    var memberPassword = row.eq(4).find('input').first().val().trim();

    var sParam = {
        seq : memberSeq,
        email : memberEmail,
        name : memberName,
        level : memberLevel,
        password: memberPassword
    }

    urlReq.put('/manage/member/' + sParam.seq, sParam, function(result) {
        if( result.error == false) {
            alert(' 정상적으로 업데이트 하였습니다. ');
            window.location.reload()
        }
        else {
            alert( result.data )
        }
    })
}

var deleteMemberInfo = function( $oJquery ) {
    var row = $oJquery.parent().siblings();

    var memberSeq = parseInt( row.eq(0).html() )

    var sParam = {
        seq : memberSeq,
    }

    if( confirm(' 고유번호 ' + memberSeq + ' 회원을 정말로 삭제하겠습니까?') ) {
       urlReq.delete('/manage/member/' + sParam.seq, sParam, function(result) {
           if( result.error == false) {
               alert(' 정상적으로 삭제하였습니다. ');
               window.location.reload()
           }
           else {
               alert( result.data )
           }
       })
    }
    return false;
}


var procAssignmentWrite = function() {
    console.log(' proc assignment write ');
    // Summernote 정보를 주입
    var summernoteContent = $('#summernote').code();
    $('#workContent').val( summernoteContent );

    return true;
}