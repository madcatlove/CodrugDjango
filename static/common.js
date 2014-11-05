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
            console.log(' final result => ' , data)
            resultCallback(data);
        })
    }


    return {
        get : function(url, data, resultCallback) {
            sAjax(url, 'GET', data, resultCallback);
        },

        post : function(url, data, resultCallback) {
            sAjax(url, 'POST', data, resultCallback);
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

    urlReq.post('/user/login', sParam, function(result) {
        if( result.error == false) {
            alert(' 정상적으로 로그인 되었습니다. ');
            $('#loginModal').modal('hide');
        }
        else {
            alert( result.errormsg );
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
        }
        else {
            alert(' 회원가입 실패. ' + result.errormsg);
        }
    })

}