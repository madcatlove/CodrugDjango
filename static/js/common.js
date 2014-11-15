/* ajax function */
var urlReq = (function() {
    var sAjax = function(url, method, data, resultCallback) {
        console.log(url, method, data)
        $.ajax({
            url: url,
            dataType: 'json',
            cache: false,
            type: method,
            data: data
        }).done( function(data) {
            console.log(' final result => ' , data, typeof(data) )
            if( typeof data === 'string')
                data = JSON.parse(data);

            resultCallback(data);
        })
    }


    return {
        get : function(url, data, resultCallback) {
            sAjax(url, 'GET', data, resultCallback);
        },

        post : function(url, data, resultCallback) {
            sAjax(url, 'POST', data, resultCallback);
        },

        put : function(url, data, resultCallback) {
            sAjax(url, 'PUT', data, resultCallback);
        },

        delete : function(url, data, resultCallback) {
            sAjax(url, 'DELETE', data, resultCallback);
        }

    }
})();



/* 로그인 실행 */
var procLogin = function() {
	var userId = $('#loginModal input').eq(0);
	var userPw = $('#loginModal input').eq(1);

	var userIdval = userId.val().trim();
	var userPwval = userPw.val().trim();

	if( userIdval.length == 0 ) {
		alert(' 아이디를 입력해주세요. ');
		userId.focus();
		return;
	}

	if( userPwval.length == 0) {
		alert(' 비밀번호를 입력해주세요. ');
		userPw.focus();
		return;
	}

	var sParam = {
        email: userIdval,
        password: userPwval,
    }

    urlReq.post('/member/login', sParam, function(result) {

        console.log( result , result.error == false)

        if( result.error == false) {
            console.log(' .... ')
            alert(' 정상적으로 로그인 되었습니다. ');
            $('#loginModal').modal('hide');
            window.location.reload();
        }
        else {
            alert( result.data );
        }

    })


}

/* 회원가입 */
var procMemberJoin = function() {
    var emailInput = $('div.memberJoinFormDiv input').eq(0);
    var passwordInput = $('div.memberJoinFormDiv input').eq(1);
    var nameInput = $('div.memberJoinFormDiv input').eq(2);

    if( emailInput.val().trim().length <= 0 ) {
        alert(' 이메일 주소를 입력해주세요. ');
        return false;
    }
    else if( passwordInput.val().trim().length <= 0 ) {
        alert(' 패스워드를 입력해주세요. ');
        return false;
    }
    else if( nameInput.val().trim().length <= 0) {
        alert(' 이름을 입력해주세요. ');
        return false;
    }

    var sParam = {
        email : emailInput.val().trim(),
        password : passwordInput.val().trim(),
        name : nameInput.val().trim()
    }

    urlReq.post('/member/join', sParam, function(result) {
        if( result.error == false) {
            alert(' 정상적으로 회원가입 되셨습니다. ');
            window.location.href = '/';
        }
        else {
            alert(' 회원가입 실패. ' + result.data);
        }
    })

}

var procMemberModify = function() {
    var currentPwd = $('div.memberModifyFormDiv input').eq(0);
    var newPwd = $('div.memberModifyFormDiv input').eq(1);
    var newPwd2 = $('div.memberModifyFormDiv input').eq(2);
    var userName = $('div.memberModifyFormDiv input').eq(3);

    if( currentPwd.val().trim().length == 0 ) {
        alert(' 현재 비밀번호를 입력하셔야 합니다. ');
        currentPwd.focus();
        return;
    }

    if( newPwd.val().trim().length != 0 ) {
        if( newPwd.val().trim() != newPwd2.val().trim() ) {
            alert(' 새로운 비밀번호가 맞지 않습니다. ');
            newPwd2.focus();
            return;
        }
    }

    if( userName.val().trim().length == 0 ) {
        alert(' 이름을 입력해 주세요. ');
        userName.focus();
        return;
    }

    sParam = {
        username : userName.val().trim(),
        userpassword : currentPwd.val().trim(),
        newpassword : newPwd.val().trim(),
        newpassword2 : newPwd2.val().trim(),
    }

    urlReq.post('/member/modify', sParam, function(result) {
        if( result.error == false) {
            alert(' 정상적으로 처리 되었습니다. ');
            window.location.href = '/';
        }
        else {
            alert( result.data );
        }
    })
}

var procMemberLogout = function() {
    urlReq.get('/member/logout', {}, function(result) {
        if( !result.error ) {
            alert( result.data );
            window.location.reload();
        }
        else {
            alert( result.data );
        }
    })
}

var viewMemberJoin = function() {
    window.location.href = '/member/join';
}


/*
    ################################
    # SUMMERNOTE UPLOAD HANDLER
    ################################
 */
var _sNote = (function() {
    var o = {};

    o.summernoteUploadHandler = function(files, editor, $welEditable) {
        console.log( files, editor, $welEditable )
	    o.summernoteUploadFile( files[0], editor, $welEditable );
    };

    o.summernoteUploadFile = function(file ,editor, $welEditable) {
        var data = new FormData();
        data.append("upFile", file);
        console.log( data )
        $.ajax({
            data: data,
            type: 'POST',
            url: '/file/upload',
            cache: false,
            contentType: false,
            processData: false,
            success: function (result) {
                console.log( result )
                result = JSON.parse(result);
                console.log( result , typeof(result) )

                if( result.error == false) {
                    var image_url = '/upload/' + result.data;
                    editor.insertImage($welEditable, image_url);
                }
                else {
                    alert(' 이미지 업로드에 실패하였습니다. ' + '(' + result.data + ')' )
                }
            }
        })
    };

    return o;
})();


var toggleWaitLayer = (function() {
    var isPoped = false; // 레이어 활성화 == true

    return function() {
        if( isPoped ) {
            $('#waitBackground').modal('hide');
            $('#waitLayer').fadeOut('fast');
            isPoped = false;
        }
        else {
            $('#waitLayer').fadeIn('fast');
            $('#waitBackground').modal({
                backdrop: 'static',
                keyboard: false,
                show: true,
            })
            isPoped = true;
        }
    }
})();