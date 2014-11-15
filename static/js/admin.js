
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

    })
}